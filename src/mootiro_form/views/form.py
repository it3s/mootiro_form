# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, sas
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
        return dict(pagetitle=pagetitle, form=form,
                    action=self.url('form', action='edit', id=form_id))

    @action(name='edit', renderer='form_edit.genshi', request_method='POST')
    @authenticated
    def save(self):
        '''Creates or updates a Form from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params
        form = Form(**extract_dict_by_prefix('form_', controls))
        form.user = self.request.user
        # Form validation passes, so create a Form in the database.
        sas.add(form)
        sas.flush()
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
        form_id = int(self.request.matchdict.get('id'))
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


