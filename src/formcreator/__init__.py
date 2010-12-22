# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.config import Configurator
from pyramid.settings import asbool
from formcreator.models import initialize_sql

def add_routes(config):
    config.add_static_view('static', 'formcreator:static')
    from views import root
    config.add_route('root', '', view=root.root, renderer='root.mako')
    # config.add_handler('hello_index', '/hello/index', handler=Hello,
    #    action='index')

    # more routes go here

def main(global_config, **settings):
    """This function returns a Pyramid WSGI application.
    """
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    config = Configurator(settings=settings)
    add_routes(config)
    return config.make_wsgi_app()
