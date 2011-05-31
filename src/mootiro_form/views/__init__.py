# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pkg_resources import resource_filename
from pyramid import interfaces
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import get_localizer, get_locale_name
from pyramid.threadlocal import get_current_request
from pyramid.url import route_url, static_url
import deform as d
from mootiro_form import package_name, _


def translator(term):
    return get_localizer(get_current_request()).translate(term)

# Add our deform templates and set deform up for i18n
deform_template_dirs = [
    resource_filename('mootiro_form', 'fieldtypes/templates'),
    resource_filename('deform', 'templates'),
]
d.Form.set_zpt_renderer(deform_template_dirs, translator=translator)


def get_button(text=_('submit')):
    '''Gets a string and generates a Deform button while setting its
    `name` attribute and capitalizing the label.
    '''
    return d.Button(title=translator(text).capitalize(),
                    name=filter(unicode.isalpha, text))


@subscriber(interfaces.IBeforeRender)
def template_globals(event):
    '''Adds stuff we use all the time to template context.
    There is no need to add *request* since it is already there.
    '''
    request = event['request']
    # A nicer "route_url": no need to pass it the request object.
    event['url_root'] = request.registry.settings['url_root']
    event['url'] = lambda name, *a, **kw: \
                          route_url(name, request, *a, **kw)
    event['static_url'] = lambda s: static_url(s, request)
    event['locale_name'] = get_locale_name(request)  # to set xml:lang
    # http://docs.pylonsproject.org/projects/pyramid_cookbook/dev/i18n.html
    localizer = get_localizer(request)
    translate = localizer.translate
    pluralize = localizer.pluralize
    event['_'] = lambda text, mapping=None: \
                 translate(text, domain=package_name, mapping=mapping)
    event['plur'] = lambda singular, plural, n, mapping=None: \
                    pluralize(singular, plural, n,
                              domain=package_name, mapping=mapping)
    # The variable enabled_locales is assigend in the main of __init__.py
    # of the application via 'import views'.
    event['enabled_locales'] = enabled_locales

"""
@subscribe(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :(
    '''
    request = event.request)
"""


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
            val = getattr(model, k)
            d[k] = val if val else ''
        return d

    def dict_to_model(self, adict, model):
        '''Helps when using Deform.'''
        for key, val in adict.items():
            setattr(model, key, val)
        return model


def authenticated(func):
    '''Decorator that redirects to the login page if the user is not yet
    authenticated.
    '''
    def wrapper(self, *a, **kw):
        if self.request.user:
            return func(self, *a, **kw)
        else:
            referrer = self.request.path
            return HTTPFound(location=self.url('user', action='login',
                _query=[('ref', referrer)]))
    return wrapper


import json
def safe_json_dumps(o, **k):
    '''The json string usually ends up inside a <script> tag. Therefore,
    if the string contains this: </script>
    ...then it must be transformed into this: <\/script>
    ...thus preserving the HTML structure of the page.
    '''
    s = json.dumps(o, indent=1, **k)
    return s.replace('/', '\/')


def print_time(msg):
    '''Decorator that prints out the time an action took to run.
    May take a message as argument.
    '''
    from datetime import datetime
    def decorator(func):
        def wrapper(*a, **kw):
            start = datetime.now()
            r = func(*a, **kw)
            print(msg + " " + str(datetime.now() - start))
            return r
        return wrapper
    return decorator
