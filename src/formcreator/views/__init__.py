# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import security, interfaces
from pyramid.events import subscriber
from pyramid.url import route_url

@subscriber(interfaces.IBeforeRender)
def template_globals(event):
    '''Adds stuff we use all the time to template context.
    There is no need to add *request* since it is already there.
    '''
    # event['route_url'] = route_url # used to build app URLs
    # A nicer "route_url": no need to pass it the request object.
    event['url'] = \
        lambda name, *a, **kw:  route_url(name, event['request'], *a, **kw)
    event['authenticated_userid'] = \
        security.authenticated_userid(event['request'])
    event['_'] = lambda x: x # Temporarily, while we don't have i18n set up.

@subscriber(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :(
    Another way to query for the user only once, might be to subclass
    AuthenticationPolicy and  def effective_principals(self, request):
    '''
    request = event.request
    request.user_id = security.authenticated_userid(request)
    if request.user_id:
        request.user = object() # TODO: retrieve user object here
    else:
        request.user = None
    print('views.on_new_request', request.user_id)


class BaseView(object):
    '''Base class for views.'''

    def __init__(self, request):
        self.request = request

    def url(self, name, *a, **kw):
        '''A route_url that is easier to use.'''
        return route_url(name, self.request, *a, **kw)

    @property
    def current_user(self):
        # userid = authenticated_userid(request)
        userid = self.request.user_id
        print('current_user:', userid)
        return sas.query(User).get(userid) if userid else None
