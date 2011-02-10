# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, sas
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
    '''Extracts information from `adict` if its key starts with `prefix` and
    returns another dictionary.
    '''
    prefix_length = len(prefix)
    return dict(((k[prefix_length:], v) for k, v in adict.items() \
                 if k.startswith(prefix)))


class FormView(BaseView):
    """The form editing view."""
    CREATE_TITLE = _('New form')
    EDIT_TITLE = _('Edit form')

    @action(name='new', renderer='form_edit.genshi', request_method='GET')
    @authenticated
    def new_form(self):
        '''Displays a new form, ready for editing.'''
        return dict(pagetitle=self.CREATE_TITLE, form=Form(name='Form Title'),
            action=self.url('form', action='new'))

    @action(name='new', renderer='form_edit.genshi', request_method='POST')
    @authenticated
    def create(self):
        '''Creates a new Form from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params
        form = Form(**extract_dict_by_prefix('form_', controls))
        form.user = self.request.user
        # Form validation passes, so create a Form in the database.
        sas.add(form)
        sas.flush()
        return HTTPFound(location=self.url('root', action='root'))

    @action(renderer='form_edit.genshi', request_method='GET')
    def edit(self):
        '''Displays the form editor, for an existing form.'''
        user = self.request.user
        return dict(pagetitle=self.EDIT_TITLE,
            user_form=user_form().render(self.model_to_dict(user,
                ('nickname', 'real_name', 'email', 'password'))))

    @action(name="delete", renderer='json', request_method='POST')
    def delete(self):
        pdict = self.request.POST

        user = self.request.user
        errors = ''

        form_id = int(pdict['formid'])
        form = filter(lambda f: f.id == form_id, user.forms)[0]

        if form:
            sas.delete(form)
            sas.flush()
            user.forms.remove(form)
        else:
            errors = _("This form doesn't exist!")

        forms_data = [ { 'form_id': form.id, 'form_name': form.name }  for form in user.forms ]

        return { 'errors': errors, 'forms': forms_data }
