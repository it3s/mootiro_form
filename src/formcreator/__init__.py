# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid_beaker import session_factory_from_settings
from formcreator.models import initialize_sql

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
authentication_policy = AuthTktAuthenticationPolicy('WeLoveCarlSagan')
authorization_policy = ACLAuthorizationPolicy()

__appname__ = 'FormCreator'

def add_routes(config):
    '''Configures all the URLs in this application.'''
    config.add_static_view('static', 'formcreator:static')
    from views import root
    config.add_route('root', '', view=root.root, renderer='root.mako',)
    # config.add_handler('hello_index', '/hello/index', handler=Hello,
    #    action='index')

    # More routes go here

def all_routes(config):
    '''Returns a list of the routes configured in this application.'''
    return [(x.name, x.pattern) for x in config.get_routes_mapper().get_routes()]

def main(global_config, **settings):
    """Returns a Pyramid WSGI application."""
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    session_factory = session_factory_from_settings(settings)
    config = Configurator(settings=settings,
                          session_factory = session_factory,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,)
    from formcreator.models.auth import User
    # Every installation of FormCreator should have its own salt (a string)
    # for creating user passwords hashes, so:
    User.salt = settings.pop('auth.password.hash.salt') # required config
    add_routes(config)
    return config.make_wsgi_app()
