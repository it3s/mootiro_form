# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import action
from formcreator.models import User, sas
from formcreator.views import BaseView
from pyramid.security import authenticated_userid, remember, forget

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
        validator=c.Length(min=8, max=40))
    # TODO: Fix password widget
    # TODO: Add a "good password" validator or something
    # TODO: Get `max` values from the model, after upgrading to SQLAlchemy 0.7

user_schema = UserSchema()

def user_form():
    '''Apparently, Deform forms must be instantiated for every request.'''
    f = d.Form(user_schema, buttons=('signup',), formid='signupform')
    f['password'].widget = d.widget.CheckedPasswordWidget()
    return f

class UserView(BaseView):
    @action(name='new', renderer='user_edit.genshi', request_method='GET')
    def new_user(self):
        '''Displays the form to create a new user.'''
        return dict(pagetitle='New user',
            user_form=user_form().render())

    @action(name='new', renderer='user_edit.genshi', request_method='POST')
    def create(self):
        '''Creates a new User from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        # print(controls)
        try:
            appstruct = user_form().validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(user_form = e.render())
        # Form validation passes, so create a User in the database.
        # print(appstruct)
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

    # TODO: add edit profile link
    @action(name='current', renderer='user_edit.genshi', request_method='GET')
    def edit_user(self):
        '''Displays the form to edit the current user profile.'''
        user = self.request.user
        # import pdb; pdb.set_trace()
        return dict(pagetitle='Edit profile',
            user_form=user_form().render(self.model_to_dict(user,
                ('nickname', 'real_name', 'email', 'password'))))

    @action(request_method='POST')
    def login(self):
        adict = self.request.params
        # print(adict)
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
