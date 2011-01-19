# -*- coding: utf-8 -*-

'''The form editor view.'''

from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid_handlers import action
from ..models import User, sas
from . import BaseView


class FormView(BaseView):
    CREATE_TITLE = 'New form'
    EDIT_TITLE = 'Edit form'

    @action(name='new', renderer='form_edit.genshi', request_method='GET')
    def new_form(self):
        '''Displays a new form, ready for editing.'''
        return dict(pagetitle=self.CREATE_TITLE)

    @action(name='new', renderer='user_edit.genshi', request_method='POST')
    def create(self):
        '''Creates a new User from POSTed data if it validates;
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

    def authenticate(self, user_id):
        '''Stores the user_id in a cookie, for subsequent requests.'''
        headers = remember(self.request, user_id) # really say user_id here?
        # May also set max_age above. (pyramid.authentication, line 272)

        # Alternate implementation:
        # headers = remember(self.request, Authenticated)
        # May also set max_age above. (pyramid.authentication, line 272)

        # Another way would be to implement session-based auth/auth.
        # session['user_id'] = user_id
        return HTTPFound(location='/', headers=headers)

    @action(name='current', renderer='user_edit.genshi', request_method='GET')
    def edit_user(self):
        '''Displays the form to edit the current user profile.'''
        user = self.request.user
        return dict(pagetitle=self.EDIT_TITLE,
            user_form=user_form().render(self.model_to_dict(user,
                ('nickname', 'real_name', 'email', 'password'))))

    @action(name='current', renderer='user_edit.genshi', request_method='POST')
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
