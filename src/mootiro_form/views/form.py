# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

import transaction
import json

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action

from mootiro_form import _
from mootiro_form.models import User, Form, sas
from mootiro_form.views import BaseView, authenticated

class FormView(BaseView):
    """The form editing view."""
    CREATE_TITLE = _('New form')
    EDIT_TITLE = _('Edit form')

    @action(name='new', renderer='form_edit.genshi', request_method='GET')
    @authenticated
    def new_form(self):
        '''Displays a new form, ready for editing.'''
        return dict(pagetitle=self.CREATE_TITLE, form=Form(name='Form Title'))

    @action(name='new', renderer='form_edit.genshi', request_method='POST')
    @authenticated
    def create(self):
        '''Creates a new Form from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        try:
            appstruct = user_form().validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.CREATE_TITLE, user_form = e.render())
        # Form validation passes, so create a User in the database.
        u = User(**appstruct)
        sas.add(u)
        sas.flush()
        return self.authenticate(u.id)

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
        forms = []

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

    @action(name='current', renderer='form_edit.genshi', request_method='POST')
    def save_user(self):
        '''Saves the user profile from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.POST.items()
        try:
            appstruct = user_form().validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.EDIT_TITLE, user_form = e.render())
        # Form validation passes, so save the User in the database.
        user = self.request.user
        self.dict_to_model(appstruct, user) # update user
        sas.flush()
        return self.authenticate(user.id)

    @action(request_method='POST')
    def login(self):
        adict = self.request.POST
        email   = adict['login_email']
        password = adict['login_pass']
        u = User.get_by_credentials(email, password)
        if u:
            return self.authenticate(u.id)
        else:
            # TODO: Redisplay the form, maybe with a...
            # self.request.session.flash(
            #    'Sorry, wrong credentials. Please try again.')
            return HTTPFound(location=self.request.referrer)

    @action(request_method='POST')
    def logout(self):
        '''Creates HTTP headers that cause the authentication cookie to be
        deleted and redirects to the front page.
        '''
        headers = forget(self.request)
        return HTTPFound(location='/', headers=headers)

    @action()
    def forgotten_password(self):
        # TODO: Implement
        return Response('forgotten_password()')


# TODO: Send e-mail and demand confirmation from the user

# TODO: Add a way to delete a user. Careful: this has enormous implications
# for the database.
