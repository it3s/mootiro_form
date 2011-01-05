# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information.'''

from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import action, view_config
from formcreator.models import User, sas
from formcreator.views import BaseView
from pyramid.security import authenticated_userid
from mako import exceptions

from schemaish import Structure, String, Invalid
from validatish.validator import Required, Length, Email, All
from formish import Form, CheckedPassword
user_schema = Structure()
user_schema.add("nickname", String(title='Nickname', \
    validator=All(Required(), Length(min=5, max=32))))
user_schema.add("real_name", String(title='Real name', \
    validator=All(Required(), Length(min=5, max=240))))
user_schema.add("email", String(title='E-mail', \
    validator=All(Required(), Email())))
user_schema.add("password", String(title='Password', \
    validator=All(Required(), Length(min=8, max=40))))
# TODO: Add a "good password" validator or something


class UserView(BaseView):
    def __init__(self, request):
        self.request = request
    
    @action(name='user', renderer='user_edit.genshi', request_method='GET')
    def show_form(self, errors=None, values=None):
        '''Displays the form to create a new user.'''
        user_form = Form(user_schema, errors=errors, defaults=values)
        user_form['password'].widget = CheckedPassword()
        return dict(user_form=user_form)
        return Response('show_form')
    
    @action(name='user', renderer='user_edit.genshi', request_method='POST')
    def create(self):
        '''Creates a new User from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        values = self.request.params
        try:
            user_schema.validate(values)
        except Invalids as e:
            print(values)
            return self.show_form(errors=e.error_dict, values=values)
        # Form validation passes, so create a User in the database.
        del values['_charset_']
        del values['password.confirm']
        values['password'] = values.pop('password.input')
        u = User(**values)
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

#Root = Root()
