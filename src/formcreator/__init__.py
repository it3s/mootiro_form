# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid_beaker import session_factory_from_settings
from formcreator.models import initialize_sql

__appname__ = 'FormCreator'

def add_routes(config):
    '''Configures all the URLs in this application.'''
    config.add_static_view('static', 'formcreator:static')
    from views import root
    config.add_route('root', '', view=root.root, renderer='root.mako')
    # config.add_handler('hello_index', '/hello/index', handler=Hello,
    #    action='index')

    # More routes go here

def all_routes(config):
    '''Returns a list of the routes configured in this application.'''
    return [(x.name, x.pattern) for x in config.get_routes_mapper().get_routes()]

''' Deprecated:
def session_factory():
    from pyramid_beaker import BeakerSessionFactoryConfig
    # http://beaker.groovie.org/modules/session.html
    # http://beaker.groovie.org/sessions.html
    # http://docs.pylonshq.com/pyramid_beaker/dev/
    return BeakerSessionFactoryConfig( \
        key = __appname__ + 'Session', # name of the cookie
        timeout = 120, # minutes to session death
    )
'''

def main(global_config, **settings):
    """This function returns a Pyramid WSGI application.
    """
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          session_factory = session_factory)
    add_routes(config)
    return config.make_wsgi_app()
