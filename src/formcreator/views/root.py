# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import action
from ..models import User, sas
from . import BaseView

class Root(BaseView):
    '''The front page of the website.'''

    @action(renderer='root.genshi')
    def root(self):
        '''
        try:
            render_to_response('root.mako', {})
        except Exception as e:
            return Response(exceptions.text_error_template().render())
        '''
        return dict()

    @action(renderer='noscript.genshi')
    def noscript(self):
        return dict()
