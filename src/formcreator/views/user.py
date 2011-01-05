# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import action, view_config
from formcreator.models import User, sas
from formcreator.views import BaseView
from pyramid.security import authenticated_userid
from mako import exceptions

import schemaish as si
from validatish.validator import Required, Length, Email, All
import formish

class user_schema(si.Structure):
    nickname  = si.String(title='Nickname',
        description="a short name for you, without spaces",
        validator=All(Required(), Length(min=5, max=32)))
    real_name = si.String(title='Real name',
        validator=All(Required(), Length(min=5, max=240)))
    email     = si.String(title='E-mail',
        validator=All(Required(), Email()))
    password  = si.String(title='Password',
        validator=All(Required(), Length(min=8, max=40)))
    # TODO: Add a "good password" validator or something
    # TODO: Get `max` values from the model, after upgrading to SQLAlchemy 0.7

user_schema = user_schema()


class UserView(BaseView):
    def __init__(self, request):
        self.request = request
    
    @action(name='user', renderer='user_edit.genshi', request_method='GET')
    def show_form(self, errors=None, values=None):
        '''Displays the form to create a new user.'''
        user_form = formish.Form(user_schema, errors=errors, defaults=values)
        user_form['password'].widget = formish.CheckedPassword()
        return dict(user_form=user_form)
        return Response('show_form')
    
    @action(name='user', renderer='user_edit.genshi', request_method='POST')
    def create(self):
        '''Creates a new User from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        postdict = self.request.params
        try:
            user_schema.validate(postdict)
        except si.Invalid as e:
            print(postdict)
            return self.show_form(errors=e.error_dict, values=postdict)
        # Form validation passes, so create a User in the database.
        del postdict['_charset_']
        del postdict['password.confirm']
        postdict['password'] = postdict.pop('password.input')
        u = User(**postdict)
        sas.add(u)
        sas.commit()
        # TODO: Authenticate this user and redirect to the inner page
        '''
        # userid = authenticated_userid(request)
        userid = self.request.user_id
        if userid is None:
            print('Not authenticated.')
            user = None
        else:
            user = sas.query(User).get(userid)
            print(user)
        '''
        return HTTPFound(location='http://example.com')
    
    @action()
    def forgotten_password(self):
        return Response('forgotten_password()')

# TODO: Send e-mail and demand confirmation from the user
