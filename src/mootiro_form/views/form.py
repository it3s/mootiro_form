# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
import json
import random
import re

import deform as d
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, Field, FieldType, Entry, sas
from mootiro_form.schemas.form import create_form_schema,\
                                      create_form_entry_schema,\
                                      form_schema,\
                                      FormTestSchema
from mootiro_form.views import BaseView, authenticated
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
        fields_json = ''
        if form_id == 'new':
            form = Form()
        else:
            form = sas.query(Form).get(form_id)

            fields_json_dict = {}
            for field in form.fields:
                fields_json_dict[field.position] = field.to_json()
            fields_json = json.dumps(fields_json_dict)

        dform = d.Form(form_schema).render(self.model_to_dict(form,
            ('name', 'description')))
        return dict(pagetitle=self._pagetitle, form=form, dform=dform, cols=2,
                    action=self.url('form', action='edit', id=form_id),
                    fields_json=fields_json, all_fieldtypes=all_fieldtypes)

    @action(name='update', renderer='json', request_method='POST')
    @authenticated
    def update(self):
        form_id = self.request.POST.get('form_id')
        request = self.request

        if form_id == 'new':
            form = Form()
            self.request.user.forms.append(form)
            sas.add(form)
        else:
            form = sas.query(Form).get(form_id)

        if form:
            # Set Title and Description
            form.name = request.POST['form_title']
            form.description = request.POST['form_desc']
            sas.flush()
            form_id = form.id

            # Get Field Positions

            field_positions = [f_idx[1] for f_idx in
                    filter(lambda fp: fp[0] == 'fields_position[]',
                                        self.request.POST.items())]

            p = 0
            positions = {}
            fp_re = re.compile('(?P<FIELD_IDX>field_\d+)')
            for fp in field_positions:
                re_fp_res = fp_re.match(fp)
                positions[re_fp_res.group('FIELD_IDX')] = p
                p += 1

            # Save/Update the fields
            fields = {}
            fa_re_str = 'fields\[(?P<FIELD_IDX>\d+)\]\[(?P<FIELD_ATTR>\w+)\]'
            fa_re = re.compile(fa_re_str)
            fields_attr = filter(lambda s: s[0].startswith('fields['),
                                                    request.POST.items())

            # Fields to delete
            deleteFields = map (lambda fid: int(fid[1]),
                                filter(lambda f: f[0] == 'deleteFields[]',
                                                    request.POST.items()))

            for f_id in deleteFields:
                # TODO: check what to do with the field answer data!!!
                field = sas.query(Field).join(Form).filter(Field.id == f_id)\
                            .filter(Form.user_id == request.user.id).first()
                sas.delete(field)

            for var_name, var_value in fields_attr:
                re_result = fa_re.match(var_name)
                idx = re_result.group('FIELD_IDX')
                attr = re_result.group('FIELD_ATTR')
                if not fields.has_key(idx):
                    fields[idx] = {}
                fields[idx][attr] = var_value

            new_fields_id = {}

            for f_idx, f in fields.items():
                if f['field_id'] == 'new':
                    field_type = sas.query(FieldType).\
                        filter(FieldType.js_proto_name == f['type']).first()
                    field = Field()
                    field.typ = field_type
                else:
                    field = sas.query(Field).get(f['field_id'])

                    if not field:
                       return {error: "Impossible to access the field"}

                # Set field label
                field.label = f['label']

                # Set if the field is required
                if f['required'] == 'true':
                    field.required = True
                else:
                    field.required = False

                # Set the field position
                field.position = positions[f['id']]

                # TODO: pass dict with all options
                # Save default value
                field.save_option('default', f['defaul'])

                # If is a new field, need to inform the client about
                # the field id on DB after a flush
                if f['field_id'] == 'new':
                    form.fields.append(field)
                    sas.flush()
                    new_fields_id[f['id']] = {'field_id': field.id}

            return {'form_id': form.id
                   ,'new_fields_id': new_fields_id}
        else:
            return {error: 'Impossible to access the form'}

    @action(name='edit', renderer='form_edit.genshi', request_method='POST')
    @authenticated
    def save_form(self):
        '''Creates or updates a Form from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        request = self.request
        form_id = request.matchdict['id']
        dform = d.Form(form_schema)
        controls = request.params.items()
        try:
            appstruct = dform.validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self._pagetitle, dform=e.render(), cols=2,
                    action=self.url('form', action='edit', id=form_id),
                    all_fieldtypes=all_fieldtypes)
        # Validation passes, so create or update the form.
        if form_id == 'new':
            form = Form(user=request.user, **appstruct)
            sas.add(form)
        else:
            form = sas.query(Form).get(form_id)
            for k, v in controls:
                setattr(form, k, v)
        sas.flush()
        # TODO: flash('The form has been saved.')
        return HTTPFound(location=self.url('root', action='root'))

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

        return HTTPFound(location=self.url('form', action='view', id=form.id))

    @action(name='tests', renderer='form_tests.genshi')
    def test(self):
        ft_schema = FormTestSchema()
        return dict(form_tests=d.Form(ft_schema, buttons=['ok']).render())

    @action(name='view', renderer='form_view.genshi')
    def view(self):
        '''Displays the form so an entry can be created.'''
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        form_schema = create_form_schema(form)
        form = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('form', action='save', id=form.id)))
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
            return dict(entries=entries)

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

    @action(name='save', renderer='form_view.genshi', request_method='POST')
    @authenticated
    def save(self):
        '''Saves the POSTed form.'''
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        form_schema = create_form_schema(form)
        dform = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('form', action='save', id=form.id)))
        submitted_data = self.request.params.items()

        try:
            form_data = dform.validate(submitted_data)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(form = e.render())

        entry = Entry()
        entry.created = datetime.utcnow()

        # Get the total number of form entries
        num_entries = sas.query(Entry).filter(Entry.form_id == form.id).count()
        entry.entry_number = num_entries + 1
        form.entries.append(entry)
        sas.add(entry)

        # This part the field data is save on DB
        # TODO: change behavior based on field type
        for f in form.fields:
            field_data = fields_dict[f.typ.name](f)
            field_data.save_data(form_data['input-{0}'.format(f.id)])
            entry.text_data.append(field_data.data)
            sas.add(field_data.data)

        return HTTPFound(location=self.url('form', action='view', id=form.id))
