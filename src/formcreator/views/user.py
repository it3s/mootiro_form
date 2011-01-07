# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import action, view_config
from formcreator.models import User, sas
from formcreator.views import BaseView
from pyramid.security import authenticated_userid, remember, Authenticated

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
    # TODO: Add a "good password" validator or something
    # TODO: Get `max` values from the model, after upgrading to SQLAlchemy 0.7

user_schema = UserSchema()

def user_form():
    '''Apparently, Deform forms must be instantiated for every request.'''
    return d.Form(user_schema, buttons=('signup',), formid='signupform')


class UserView(BaseView):
    @action(name='user', renderer='user_edit.genshi', request_method='GET')
    def show_form(self):
        '''Displays the form to create a new user.'''
        return dict(user_form=user_form().render())

    @action(name='user', renderer='user_edit.genshi', request_method='POST')
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
        print('YEAH, FLUSH!!!11', u.id)
        self.remember(u.id)
        return HTTPFound(location='/')

    def remember(self, user_id):
        '''Authenticates the user so the web server will know who they are in
        subsequent requests.
        '''
        remember(self.request, user_id) # Can I really use user_id here?
        # May also set max_age above. (pyramid.authentication, line 272)

        # Alternate implementation:
        # remember(self.request, Authenticated)
        # May also set max_age above. (pyramid.authentication, line 272)
        # session['user_id'] = user_id

        # Another way would be to implement session-based auth/auth.


    @action()
    def forgotten_password(self):
        return Response('forgotten_password()')

# TODO: Send e-mail and demand confirmation from the user
# pyramid.security.Authenticated
