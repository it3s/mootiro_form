# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import get_localizer, get_locale_name
from pyramid.threadlocal import get_current_request
from pyramid.url import route_url, static_url
from mootiro_web.user import BaseView, authenticated
from mootiro_form import package_name, _


"""
from pyramid import interfaces
from pyramid.events import subscriber
@subscribe(interfaces.INewRequest)
def on_new_request(event):
    '''This is being called for static requests too :(
    '''
    request = event.request)
"""


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
