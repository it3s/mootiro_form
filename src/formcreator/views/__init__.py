# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import security, interfaces
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from ..models.auth import User, sas

@subscriber(interfaces.IBeforeRender)
def template_globals(event):
    '''Adds stuff we use all the time to template context.
    There is no need to add *request* since it is already there.
    '''
    # event['route_url'] = route_url # used to build app URLs
    # A nicer "route_url": no need to pass it the request object.
    event['url'] = \
        lambda name, *a, **kw:  route_url(name, event['request'], *a, **kw)
    event['_'] = lambda x: x # Temporarily, while we don't have i18n set up.

"""
@subscriber(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :(
    '''
    request = event.request)
"""


from pyramid.request import Request

class MyRequest(Request):
    @reify
    def user(self):
        '''Memoized user object. If we always use request.user to retrieve
        the authenticated user, the query will happen only once per request,
        which is good for performance.
        '''
        userid = authenticated_userid(self)
        print('current user id:', userid)
        return sas.query(User).get(userid) if userid else None


class BaseView(object):
    '''Base class for views.'''

    def __init__(self, request):
        self.request = request

    def url(self, name, *a, **kw):
        '''A route_url that is easier to use.'''
        return route_url(name, self.request, *a, **kw)

    def model_to_dict(self, model, keys):
        d = {}
        for k in keys:
            d[k] = getattr(model, k)
        return d
