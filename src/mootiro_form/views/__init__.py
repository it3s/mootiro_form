# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import security, interfaces
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.i18n import get_localizer, get_locale_name
from pyramid.request import Request
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from .. import package_name
from ..models import User, sas

@subscriber(interfaces.IBeforeRender)
def template_globals(event):
    '''Adds stuff we use all the time to template context.
    There is no need to add *request* since it is already there.
    '''
    request = event['request']
    # A nicer "route_url": no need to pass it the request object.
    event['url'] = lambda name, *a, **kw: \
                          route_url(name, request, *a, **kw)
    event['locale_name'] = get_locale_name(request) # to set xml:lang
    # http://docs.pylonsproject.org/projects/pyramid_cookbook/dev/i18n.html
    localizer = get_localizer(request)
    translate = localizer.translate
    pluralize = localizer.pluralize
    event['_'] = lambda text, mapping=None: \
                 translate(text, domain=package_name, mapping=mapping)
    event['plur'] = lambda singular, plural, n, mapping=None: \
                    pluralize(singular, plural, n,
                              domain=package_name, mapping=mapping)

"""
@subscriber(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :(
    '''
    request = event.request)
"""


class MyRequest(Request):
    @reify
    def user(self):
        '''Memoized user object. If we always use request.user to retrieve
        the authenticated user, the query will happen only once per request,
        which is good for performance.
        '''
        userid = authenticated_userid(self)
        return sas.query(User).get(userid) if userid else None


class BaseView(object):
    '''Base class for views.'''

    def __init__(self, request):
        self.request = request

    @reify
    def tr(self):
        return get_localizer(self.request).translate

    def url(self, name, *a, **kw):
        '''A route_url that is easier to use.'''
        return route_url(name, self.request, *a, **kw)

    def model_to_dict(self, model, keys):
        '''Helps when using Deform.'''
        d = {}
        for k in keys:
            d[k] = getattr(model, k)
        return d

    def dict_to_model(self, adict, model):
        '''Helps when using Deform.'''
        for key, val in adict.items():
            setattr(model, key, val)
        return model
