# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import action, view_config
from formcreator.models import User, sas
from formcreator.views import BaseView
from pyramid.security import authenticated_userid
from mako import exceptions

class UserView(BaseView):
    def __init__(self, request):
        self.request = request
    
    @action(name='user', renderer='user_edit.genshi', request_method='GET')
    def show_form(self):
        '''Displays the form to create a new user.'''
        return dict()
        return Response('show_form')
    
    @action(name='user', renderer='root.mako', request_method='POST')
    def create(self):
        '''Creates a new User from POSTed data.'''
        return Response('create user')
        print('root:', self.request)
        # userid = authenticated_userid(request)
        userid = self.request.user_id
        if userid is None:
            print('Not authenticated.')
            user = None
        else:
            user = sas.query(User).get(userid)
            print(user)
        '''
        try:
            render_to_response('root.mako', {})
        except Exception as e:
            return Response(exceptions.text_error_template().render())
        '''    
        return dict(user=user)
    
    @action()
    def forgotten_password(self):
        return Response('forgotten_password()')

#Root = Root()
