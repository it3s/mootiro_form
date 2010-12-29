# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import security, interfaces
from pyramid.events import subscriber

@subscriber(interfaces.IBeforeRender)
def add_globals(event):
    '''Adds stuff we use all the time in templates.'''
    # print('\n{0}\n'.format(event['request']))
    event['authenticated_userid'] = \
        security.authenticated_userid(event['request'])
    event['_'] = lambda x: x # Temporarily, while we don't have i18n set up.
