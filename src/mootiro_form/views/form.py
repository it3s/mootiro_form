# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import random
import csv
import deform as d

from cStringIO import StringIO
from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form import _
from mootiro_form.utils.form import make_form
from mootiro_form.models import Form, FormCategory, Field, FieldType, Entry, sas
from mootiro_form.schemas.form import create_form_schema,\
                                      create_form_entry_schema,\
                                      form_schema,\
                                      FormTestSchema
from mootiro_form.views import BaseView, authenticated
from mootiro_form.utils.text import random_word
from mootiro_form.fieldtypes import all_fieldtypes, fields_dict


def pop_by_prefix(prefix, adict):
    '''Pops information from `adict` if its key starts with `prefix` and
    returns another dictionary.
    '''
    prefix_length = len(prefix)
    d = {}
    for k in adict:
        if k.startswith(prefix):
            d[k[prefix_length:]] = adict.pop(k)
    return d


def extract_dict_by_prefix(prefix, adict):
    '''Reads information from `adict` if its key starts with `prefix` and
    returns another dictionary.
    '''
    prefix_length = len(prefix)
    return dict(((k[prefix_length:], v) for k, v in adict.items() \
                 if k.startswith(prefix)))


class FormView(BaseView):
    """The form editing view."""
    CREATE_TITLE = _('New form')
    EDIT_TITLE = _('Edit form')

    @property
    def _pagetitle(self):
        id = self.request.matchdict['id']
        return self.CREATE_TITLE if id == 'new' else self.EDIT_TITLE

    @action(name='edit', renderer='form_edit.genshi', request_method='GET')
    @authenticated
    def show_edit(self):
        '''Displays the form editor, for new or existing forms.'''
        form_id = self.request.matchdict['id']
        if form_id == 'new':
            form = Form()
            fields_json = json.dumps([])
        else:
            form = sas.query(Form).get(form_id)
            fields_json = json.dumps( \
                [f.to_json() for f in form.fields], indent=1)
            # (indent=1 causes the serialization to be much prettier.)
        dform = d.Form(form_schema, formid='FirstPanel') \
            .render(self.model_to_dict(form, ('name', 'description')))
        return dict(pagetitle=self._pagetitle, form=form, dform=dform,
                    action=self.url('form', action='edit', id=form_id),
                    fields_json=fields_json, all_fieldtypes=all_fieldtypes)

    @action(name='edit', renderer='json', request_method='POST')
    @authenticated
    def save_form(self):
        '''Responds to the AJAX request and saves a form with its fields.'''
        request = self.request
        posted = json.loads(request.POST.pop('json'))
        # Validate the form panel (especially form name length)
        form_props = [('_charset_', ''),
            ('__formid__', 'FirstPanel'),
            ('name', posted['form_title']),
            ('description', posted['form_desc']),
        ]
        dform = d.Form(form_schema, formid='FirstPanel')
        try:
            dform.validate(form_props)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            rd = dict(panel_form=e.render(), error='Form properties error')
            return rd
        else:
            panel_form = dform.render(form_props)
        # Validation passes, so create or update the form.
        form_id = posted['form_id']
        if form_id == 'new':
            form = Form(user=request.user)
            sas.add(form)
        else:
            form = sas.query(Form).get(form_id)
            if not form:
                return dict(error=_('Form not found!'))

        # Set form properties
        form.name = posted['form_title']
        form.description = posted['form_desc']
        form.public = posted['form_public']

        if form.public:
            if not form.slug:
                # Generates unique new slug
                s = random_word(10)
                while sas.query(Form).filter(Form.slug == s).first():
                    s = random_word(10)
                form.slug = s

        form.thanks_message = posted['form_thanks_message']

        if form_id == 'new':
            sas.flush()  # so we get the form id

        # Get field positions
        positions = {f[:-len("_container")]: p for p, f in \
                            enumerate(posted['fields_position'])}

        # Save/Update the fields
        # Fields to delete
        for f_id in posted['deleteFields']:
            # TODO: check what to do with the field answer data!!!
            field = sas.query(Field).join(Form).filter(Field.id == f_id)\
                        .filter(Form.user_id == request.user.id).first()
            sas.delete(field)

        new_fields_id = {}
        save_options_result = {}
        for f in posted['fields']:
            if f['field_id'] == 'new':
                field_type = sas.query(FieldType).\
                    filter(FieldType.name == f['type']).first()
                field = Field()
                field.typ = field_type
            else:
                field = sas.query(Field).get(f['field_id'])
                if not field:
                    return dict(error="Field not found: {}" \
                        .format(f['field_id']))

            f['position'] = positions[f['id']]
            opt_result = field.save_options(f)
            if opt_result:
                save_options_result[f['id']] = opt_result

            # If is a new field, need to inform the client about
            # the field id on DB after a flush
            if f['field_id'] == 'new':
                form.fields.append(field)
                sas.flush()
                new_fields_id[f['id']] = {'field_id': field.id}

        rdict = {'form_id': form.id,
                'new_fields_id': new_fields_id,
                'save_options_result': save_options_result,
                'panel_form': panel_form,
                }
        if form.slug:
            rdict['form_public_url'] = self.url('form_slug', action='view',
                slug=form.slug)

        return rdict

    @action(renderer='json', request_method='POST')
    @authenticated
    def rename(self):
        form_id = self.request.matchdict['id']
        form_name = self.request.POST['form_name']
        form = sas.query(Form).filter(Form.id == form_id).first()
        if form:
            form.name = form_name
            errors = ''
        else:
            errors = _("Error finding form")
        return {'errors': errors}

    @action(renderer='json', request_method='POST')
    @authenticated
    def delete(self):
        user = self.request.user
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == user).first()
        if form:
            sas.delete(form)
            sas.flush()
            errors = ''
        else:
            errors = _("This form doesn't exist!")
        if user.forms:
            forms_data = json.dumps([form.to_json() for form in user.forms])
        else:
            forms_data = ''
        return {'errors': errors, 'forms': forms_data}

    @action(name='category_show_all', renderer='category_show.genshi',
            request_method='GET')
    @authenticated
    def category_show(self):
        categories = sas.query(FormCategory).all()
        return categories

    @action(name='tests', renderer='form_tests.genshi', request_method='POST')
    @authenticated
    def generate_tests(self):
        request = self.request
        form_id = int(self.request.matchdict['id'])
        ft_form = d.Form(FormTestSchema())
        controls = request.params.items()
        try:
            form_data = ft_form.validate(controls)
        except d.ValidationFailure as e:
            return dict(form_tests=e.render())

        # Get the form to add the test fields
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        field_types = []
        total_fields = form_data['nfields_ti'] + form_data['nfields_ta']

        field_types.append((form_data['nfields_ti'],
                sas.query(FieldType).filter(FieldType.name == 'Text').first()))
        field_types.append((form_data['nfields_ta'],
                sas.query(FieldType).filter(FieldType.name == 'TextArea') \
                    .first()))

        # Random Order
        order = range(0, total_fields)
        random.shuffle(order)

        for f in form.fields:
            sas.delete(f)

        def add_field(typ, field_num, field_pos):
            new_field = Field()
            new_field.label = '{0} {1}'.format(typ.name, field_num)
            new_field.help_text = 'help of {0} {1}'.format(typ.name, field_num)
            new_field.description = 'desc of {0} {1}' \
                .format(typ.name, field_num)
            new_field.position = field_pos
            new_field.required = random.choice([True,False])
            new_field.typ = typ
            form.fields.append(new_field)
            sas.add(new_field)

        for f in field_types:
            for i in xrange(0, f[0]):
                pos = order.pop()
                add_field(f[1], i, pos)

        return HTTPFound(location=self.url('form_slug', action='view', id=form.id))

    @action(name='tests', renderer='form_tests.genshi')
    def test(self):
        ft_schema = FormTestSchema()
        return dict(form_tests=d.Form(ft_schema, buttons=['ok']).render())

    @action(name='view', renderer='form_view.genshi')
    def view(self):
        '''Displays the form so an entry can be created.'''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        if form == None:
            return HTTPNotFound()
        if not form.public:
            return dict(not_published=True)

        form_schema = create_form_schema(form)
        form = make_form(form_schema, i_template='form_mapping_item',
                buttons=['Ok'],
                action=(self.url('form_slug', action='save_answer', slug=form.slug)))
        return dict(form=form.render())

    @action(name='entry', renderer='form_view.genshi')
    @authenticated
    def entry(self):
        '''Displays one entry to the facilitator.'''
        entry_id = int(self.request.matchdict['id'])
        entry = sas.query(Entry).filter(Entry.id == entry_id).first()

        if entry:
            # Get the answers
            form_entry_schema = create_form_entry_schema(entry)
            entry_form = d.Form(form_entry_schema)
            return dict(form = entry_form.render())

    @action(name='answers', renderer='form_answers.genshi')
    @authenticated
    def answers(self):
        '''Displays a list of the entries of a form.'''
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        if form:
            # Get the answers
            entries = sas.query(Entry).filter(Entry.form_id == form.id).all()
            return dict(entries=entries, form_id=form_id)

    @action(name='filter', renderer='form_answers.genshi')
    @authenticated
    def filter_entries(self):
        '''Group and filter the form's entries'''
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        if form:
            # Get the answers
            entries = sas.query(Entry).filter(Entry.form_id == form.id).all()
            return dict(entries=entries)

    @action(name='save_answer', renderer='form_view.genshi', request_method='POST')
    def save_answer(self):
        '''Saves an answer POSTed to the form, and stores a new entry to it.'''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        form_schema = create_form_schema(form)
        dform = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('form_slug', action='view', slug=form.slug)))
        submitted_data = self.request.params.items()

        try:
            form_data = dform.validate(submitted_data)
        except d.ValidationFailure as e:
            return dict(form = e.render())

        entry = Entry()
        entry.created = datetime.utcnow()

        # Get the total number of form entries
        num_entries = sas.query(Entry).filter(Entry.form_id == form.id).count()
        entry.entry_number = num_entries + 1
        form.entries.append(entry)
        sas.add(entry)
        sas.flush()

        # This part the field data is save on DB
        for f in form.fields:
            field_data = fields_dict[f.typ.name](f)
            field_data.save_data(entry, form_data['input-{0}'.format(f.id)])

        return HTTPFound(location=self.url('form_slug', action='thank', slug=form.slug))

    @action(name='thank', renderer='form_view.genshi')
    def thank(self):
        '''After saving an answer and creating a new entry for the form thank
        the person who aswered it.'''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        tm = form.thanks_message if form.thanks_message \
                else _("We've received you submission. Thank you.")

        return dict(thanks_message=tm)

    def _csv_generator(self, form_id, encoding='utf-8'):
        '''A generator that returns the entries of a form line by line'''
        form = sas.query(Form).filter(Form.id == form_id).one()
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        # write column names 
        column_names = [self.tr(_('Entry'))] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        for e in form.entries:
            # get the data of the fields of the entry e in a list
            fields_data = [e.entry_number] + \
                          [f.value(e).encode(encoding) for f in form.fields]
            # generator which returns one row of the csv file (=data of the
            # fields of the entry e)
            csvWriter.writerow(fields_data)
            row = file.getvalue()
            file.seek(0)
            file.truncate()
            yield row
        sas.remove()

    @action(name='export', request_method='GET')
    @authenticated
    def create_csv(self):
        '''Exports the entries to a form as csv file and initializes
        download from the server''' 
        form_id = self.request.matchdict['id']
        # Assign name of the file dynamically according to form name and
        # creation date
        form = sas.query(Form).filter(Form.id == form_id).one()
        name = self.tr(_('Answers_to_{0}_{1}.csv')) \
            .format(form.name, unicode(form.created)[:10])
        # Initialize download while creating the csv file by passing a
        # generator to app_iter. To avoid SQL Alchemy session problems sas is
        # called again in csv_generator instead of passing the form object
        # directly.
        return Response(status='200 OK',
               headerlist=[('Content-Disposition', 'attachment; filename={0}' \
                          .format(name))],
               app_iter=self._csv_generator(form_id))

