# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import security, interfaces
from pyramid.events import subscriber

@subscriber(interfaces.IBeforeRender)
def add_globals(event):
    '''Adds stuff we use all the time in templates.'''
    # print('\n{0}\n'.format(event['request']))
    print('add_globals')
    event['authenticated_userid'] = \
        security.authenticated_userid(event['request'])
    event['_'] = lambda x: x # Temporarily, while we don't have i18n set up.

@subscriber(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :( '''
    request = event.request
    request.user_id = security.authenticated_userid(request)
    if request.user_id:
        request.user = object() # TODO: retrieve user object here
    else:
        request.user = None
    print('on_new_request', type(event), request.user_id)

