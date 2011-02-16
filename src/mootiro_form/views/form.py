# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
import random
import colander as c
import deform as d
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, Field, FieldType, Entry, sas, TextInputData
from mootiro_form.schemas.form import create_form_schema, form_schema, FormTestSchema
from mootiro_form.views import BaseView, authenticated


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

    @action(name='edit', renderer='form_edit.genshi', request_method='GET')
    @authenticated
    def show_edit(self):
        '''Displays the form editor, for new or existing forms.'''
        form_id = self.request.matchdict.get('id')
        if form_id == 'new':
            pagetitle = self.CREATE_TITLE
            form = Form()
        else:
            pagetitle = self.EDIT_TITLE
            form = sas.query(Form).get(form_id)
        dform = d.Form(form_schema).render(self.model_to_dict(form, ('name',)))
        #import pdb; pdb.set_trace()
        return dict(pagetitle=pagetitle, form=form, dform=dform,
                    action=self.url('form', action='edit', id=form_id))

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
            return dict(pagetitle=self.CREATE_TITLE, dform=e.render(),
                    action=self.url('form', action='edit', id=form_id))
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
        forms_data = [{'form_id': form.id, 'form_name': form.name} \
                     for form in user.forms]

        return {'errors': errors, 'forms': forms_data}

    @action(name='category_show_all', renderer='category_show.genshi',
            request_method='GET')
    def category_show(self):
        categories = sas.query(FormCategory).all()
        return categories

    @action(name='tests', renderer='form_tests.genshi', request_method='POST')
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
                sas.query(FieldType).filter(FieldType.name == 'TextInput').first()))
        field_types.append((form_data['nfields_ta'],
                sas.query(FieldType).filter(FieldType.name == 'TextArea').first()))

        # Random Order
        order = range(0, total_fields)
        random.shuffle(order)

        for f in form.fields:
            sas.delete(f)

        def add_field(typ, field_num, field_pos):
            new_field = Field()
            new_field.label = '{0} {1}'.format(typ.name, field_num)
            new_field.help_text = 'help of {0} {1}'.format(typ.name, field_num)
            new_field.description = 'desc of {0} {1}'.format(typ.name, field_num)
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

    @action(name="view", renderer='form_view.genshi')
    def view(self):
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        form_schema = create_form_schema(form)
        form = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('form', action='save', id=form.id)))
        return dict(form=form.render())

    @action(name='save', renderer='form_view.genshi', request_method='POST')
    def save(self):
        form_id = int(self.request.matchdict['id'])
        form = sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

        form_schema = create_form_schema(form)
        dform = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('form', action='save', id=form.id)))
        submited_data = self.request.params.items()

        try:
            form_data = dform.validate(submited_data)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(form = e.render())

        entry = Entry()
        entry.created = datetime.utcnow()
        form.entries.append(entry)
        sas.add(entry)

        for field in form.fields:
            data = TextInputData()
            data.field_id = field.id
            data.value = form_data['input-{0}'.format(field.id)]
            entry.textinput_data.append(data)
            sas.add(data)

        return HTTPFound(location=self.url('form', action='view', id=form.id))


