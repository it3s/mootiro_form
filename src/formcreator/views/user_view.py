# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid_handlers import action
from ..models import User, sas
from . import BaseView

import colander as c
import deform   as d

class UserSchema(c.MappingSchema):
    nickname  = c.SchemaNode(c.Str(), title='Nickname',
        description="a short name for you, without spaces", size=20,
        validator=c.Length(min=5, max=32))
    real_name = c.SchemaNode(c.Str(), title='Real name',
        validator=c.Length(min=5, max=240))
    email     = c.SchemaNode(c.Str(), title='E-mail',
        validator=c.Email())
    password  = c.SchemaNode(c.Str(), title='Password',
        validator=c.Length(min=8, max=40),
        widget = d.widget.CheckedPasswordWidget())
    # TODO: Fix password widget appearance (in CSS?)
    # TODO: Add a "good password" validator or something. Here are some ideas:
        # must be 6-20 characters in length
        # must have at least one number and one letter
        # must be different from the username and email
        # can contain spaces?
        # is case-sensitive.
    # TODO: Get `max` values from the model, after upgrading to SQLAlchemy 0.7

user_schema = UserSchema()

from bag.text import filter_chars_in
def user_form(button='submit'):
    '''Apparently, Deform forms must be instantiated for every request.'''
    # TODO: I realize the interface to this function is stupid because it is not
    # i18n resistant.
    button = d.Button(title=button.capitalize(),
                      name=filter_chars_in(button, unicode.isalpha))
    return d.Form(user_schema, buttons=(button,), formid='userform')


class UserView(BaseView):
    CREATE_TITLE = 'New user'
    EDIT_TITLE = 'Edit profile'

    @action(name='new', renderer='user_edit.genshi', request_method='GET')
    def new_user(self):
        '''Displays the form to create a new user.'''
        return dict(pagetitle=self.CREATE_TITLE,
            user_form=user_form('sign up').render())

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
