# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid_handlers import action
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

    @action()
    def favicon(self):
        settings = self.request.registry.settings
        icon = open(settings['favicon'], 'r')
        return Response(content_type=settings['favicon_content_type'],
                        app_iter=icon)

    @action()
    def locale(self):
        '''Sets the locale cookie and redirects back to the referer page.'''
        location = self.request.referrer
        if not location:
            location = '/'
        locale = self.request.matchdict['locale']
        settings = self.request.registry.settings
        if locale in settings['enabled_locales']:
            headers = [('Set-Cookie',
                '_LOCALE_={0}; expires=31 Dec 2050 23:00:00 GMT; Path=/'.format(locale))]
        else:
            headers = None
        return HTTPFound(location=location, headers=headers)
