# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import random
import csv
import deform as d
import colander as c

from datetime import datetime
from cStringIO import StringIO
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, Field, FieldType, Entry, sas
from mootiro_form.schemas.form import form_schema, \
                                      form_name_schema, FormTestSchema
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
        fields_config_json = json.dumps({ft[0]: ft[1](Field()).initJson() \
                                         for ft in fields_dict.items()})
        if form_id == 'new':
            form = Form()
            fields_json = json.dumps([])
        else:
            form = sas.query(Form).get(form_id)
            fields_json = json.dumps( \
                [f.to_dict() for f in form.fields], indent=1)
            # (indent=1 causes the serialization to be much prettier.)
        dform = d.Form(form_schema, formid='FirstPanel') \
            .render(self.model_to_dict(form, ('name', 'description',
                    'submit_label')))

        # Field types class names
        fieldtypes_json = json.dumps([typ.__class__.__name__ \
                                    for typ in all_fieldtypes])

        return dict(pagetitle=self._pagetitle, form=form, dform=dform,
                    action=self.url('form', action='edit', id=form_id),
                    fields_json=fields_json, all_fieldtypes=all_fieldtypes,
                    fieldtypes_json=fieldtypes_json,
                    fields_config_json=fields_config_json)

    @action(name='edit', renderer='json', request_method='POST')
    @authenticated
    def save_form(self):
        '''Responds to the AJAX request and saves a form with its fields.'''
        request = self.request
        posted = json.loads(request.POST.pop('json'))
        # Validate the form panel (especially form name length)
        # TODO: Using deform for this was a mistake. We should use colander
        # only, and display errors using javascript, as we did on the
        # following method "rename".
        form_props = [('_charset_', ''),
            ('__formid__', 'FirstPanel'),
            ('name', posted['form_title']),
            ('description', posted['form_desc']),
            ('submit_label', posted['submit_label'])
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
            form = self._get_form_if_belongs_to_user(form_id=form_id)
            if not form:
                return dict(error=_('Form not found!'))

        # Set form properties
        form.name = posted['form_title']
        form.description = posted['form_desc']
        form.public = posted['form_public']
        form.submit_label = posted['submit_label']
        form.modified = datetime.utcnow()

        if form.public:
            if not form.slug:
                # Generates unique new slug
                s = random_word(10)
                while sas.query(Form).filter(Form.slug == s).first():
                    s = random_word(10)
                form.slug = s

        form.thanks_message = posted['form_thanks_message']

        # Validation for start and end date
        # TODO Jan, still KeyError if "posted['start_date']" instead of:
        if posted.get('start_date', ''):
            form.start_date = datetime.strptime(posted['start_date'],
                                                "%Y-%m-%d %H:%M")
        else:
            form.start_date = None
        if posted['end_date']:
            form.end_date = datetime.strptime(posted['end_date'],
                                              "%Y-%m-%d %H:%M")
        else:
            form.end_date = None

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
            if not f['field_id']:
                raise RuntimeError('Cannot instantiate a field of ID {}' \
                    .format(f['field_id']))
            elif f['field_id'] == 'new':
                field_type = sas.query(FieldType).\
                    filter(FieldType.name == f['type']).first()
                # To solve a bug where field.save_options() would fail because
                # of a missing field ID, we instantiate the field here and flush
                field = Field(typ=field_type, form=form, label=f['label'],
                    description=f['description'], help_text=None)
                sas.add(field)
                sas.flush()
                # TODO: Populating the above instance variables is probably
                # redundantly done elsewhere, but it must be done here.
            else:
                field = sas.query(Field).get(f['field_id'])
                if not field:
                    return dict(error="Field not found: {}" \
                        .format(f['field_id']))

            f['position'] = positions[f['id']]
            # Before calling this, the field must have an ID:
            opt_result = field.save_options(f)
            if opt_result:
                save_options_result[f['id']] = opt_result

            # If is a new field, need to inform the client about
            # the field id on DB after a flush
            if f['field_id'] == 'new':
                sas.flush()
                new_fields_id[f['id']] = {'field_id': field.id}

        rdict = {'form_id': form.id,
                'new_fields_id': new_fields_id,
                'save_options_result': save_options_result,
                'panel_form': panel_form,
                }
        if form.slug:
            rdict['form_public_url'] = self.url('entry_form_slug',
                action='view_form', slug=form.slug)

        return rdict

    def _get_form_if_belongs_to_user(self, form_id=None, key='id'):
        '''Returns the form instance indicated by matchdict[key],
        as long as it belongs to the current user.
        '''
        if not form_id:
            form_id = self.request.matchdict[key]
        return sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

    @action(renderer='json', request_method='POST')
    @authenticated
    def rename(self):
        # 1. Validate form name length, using only Colander
        new_name = self.request.POST['form_name']
        try:
            form_name_schema.deserialize(new_name)
        except c.Invalid as e:
            return e.asdict()  # {'name': u'Longer than maximum length 255'}
        # 2. Retrieve the form model
        form = self._get_form_if_belongs_to_user()
        if not form:
            return dict(name=_("Error finding form"))
        # 3. Save the new name, return OK
        form.name = new_name
        return {'name': ''}

    @action(renderer='json', request_method='POST')
    @authenticated
    def delete(self):
        form = self._get_form_if_belongs_to_user()
        if form:
            sas.delete(form)
            sas.flush()
            error = ''
        else:
            error = _("This form doesn't exist!")
        user = self.request.user
        all_data = user.all_categories_and_forms()
        return {'errors': error, 'all_data': all_data}

    @action(name='copy', renderer='json', request_method='POST')
    @authenticated
    def copy(self):
        form = self._get_form_if_belongs_to_user()
        if form:
            form_copy = form.copy()
            form_copy.name += " " + _("(copy)")
            sas.flush()
            error = ''
        else:
            error = _("This form doesn't exist!")

        user = self.request.user
        all_data = user.all_categories_and_forms()
        return {'errors': error, 'all_data': all_data,
            'form_copy_id': form_copy.id}

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

        return HTTPFound(location=self.url('entry_form_slug',
                    action='view_form', id=form.id))

    @action(name='tests', renderer='form_tests.genshi')
    def test(self):
        ft_schema = FormTestSchema()
        return dict(form_tests=d.Form(ft_schema, buttons=['ok']).render())

    @action(name='entry', renderer='form_view.genshi')
    @authenticated
    def entry(self):
        '''Displays one entry to the facilitator.'''
        entry_id = int(self.request.matchdict['id'])
        entry = sas.query(Entry).filter(Entry.id == entry_id).first()

        if entry:
            # Get the entries
            form_entry_schema = create_form_schema(entry.form)
            entry_form = d.Form(form_entry_schema)
            return dict(form = entry_form.render())

    @action(name='answers', renderer='form_answers.genshi')
    @authenticated
    def answers(self):
        '''Displays a list of the entries of a form.'''
        form_id = int(self.request.matchdict['id'])
        form = self._get_form_if_belongs_to_user(form_id)
        # TODO: if not form:
        # Get the answers
        entries = sas.query(Entry).filter(Entry.form_id == form.id).all()
        return dict(form=form, entries=entries, form_id=form.id)

    @action(name='filter', renderer='form_answers.genshi')
    @authenticated
    def filter_entries(self):
        '''Group and filter the form's entries'''
        form = self._get_form_if_belongs_to_user('form_id')
        # TODO: if not form:
        # Get the answers
        entries = sas.query(Entry).filter(Entry.form_id == form.id).all()
        return dict(entries=entries)

    def _csv_generator(self, form_id, encoding='utf-8'):
        '''A generator that returns the entries of a form line by line.
        '''
        form = sas.query(Form).filter(Form.id == form_id).one()
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        # write column names
        column_names = [self.tr(_('Entry')),
                        self.tr(_('Submissions (Date, Time)'))] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        for e in form.entries:
            # get the data of the fields of the entry e in a list
            fields_data = [e.entry_number, str(e.created)[:16]] + \
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
        download from the server.
        '''
        form = self._get_form_if_belongs_to_user()
        # Assign name of the file dynamically according to form name and
        # creation date. Have to cut the name to have a max filename lenght
        # of 255 Characters. More is not supported by the os.
        name = self.tr(_('Entries_to_{0}_{1}.csv')) \
                .format(unicode(form.name[:200]).replace(' ','_'),
                        unicode(form.created)[:10])
        print name
        # Initialize download while creating the csv file by passing a
        # generator to app_iter. To avoid SQL Alchemy session problems sas is
        # called again in csv_generator instead of passing the form object
        # directly.
        return Response(status='200 OK',
               headerlist=[(b'Content-Type', b'text/comma-separated-values'),
                    (b'Content-Disposition', b'attachment; filename={0}' \
                    .format(name.encode('utf8')))],
               app_iter=self._csv_generator(form.id))
