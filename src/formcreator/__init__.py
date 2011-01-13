# -*- coding: utf-8 -*-
'''Main configuration of FormCreator.'''

from __future__ import unicode_literals # unicode by default

from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid_beaker import session_factory_from_settings
from .models import initialize_sql
from .views import MyRequest

__appname__ = 'FormCreator'

def add_routes(config):
    '''Configures all the URLs in this application.'''
    config.add_static_view('static', 'formcreator:static')
    # The *Deform* form creation library uses this:
    config.add_static_view('deform', 'deform:static')
    # config.add_route('root', '', view=root.root, renderer='root.mako',)
    handler = config.add_handler
    handler('root', '', handler='formcreator.views.root.Root', action='root')
    handler('noscript', 'noscript', handler='formcreator.views.root.Root',
            action='noscript')
    handler('user', 'user/{action}', handler='formcreator.views.user.UserView')
    # handler(’hello’, ’/hello/{action}’, handler=Hello)

def all_routes(config):
    '''Returns a list of the routes configured in this application.'''
    return [(x.name, x.pattern) for x in \
            config.get_routes_mapper().get_routes()]

def find_groups(userid, request):
    '''TODO: Upgrade this function if we ever use Pyramid authorization.
    Used by the authentication policy; should return a list of
    group identifiers or None.
    Apparently, authenticated_userid() invokes this when there is an
    authenticated user.
    '''
    # user = request.user
    # Maybe catch NoResultFound, MultipleResultFound, and possibly
    # return user.groups list instead of [] if we end up having groups
    return []

def auth_tuple():
    '''Returns a tuple of 2 auth/auth objects, for configuration.'''
    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy
    return (AuthTktAuthenticationPolicy \
        ('WeLoveCarlSagan', callback=find_groups, include_ip=True),
         None) # ACLAuthorizationPolicy())

def config_dict(settings):
    '''Returns the Configurator parameters.'''
    auth = auth_tuple()
    return dict(settings=settings,
                request_factory = MyRequest,
                session_factory = session_factory_from_settings(settings),
                authentication_policy = auth[0],
                authorization_policy = auth[1],
    )

def enable_kajiki(config):
    '''Allows us to use the Kajiki templating language.'''
    from bag.web.pyramid_kajiki import renderer_factory
    for extension in ('.txt', '.xml', '.html', '.html5'):
        config.add_renderer(extension, renderer_factory)

def enable_genshi(config):
    '''Allows us to use the Genshi templating language.
    We intend to switch to Kajiki down the road, therefore it would be best to
    avoid py:match.
    '''
    from bag.web.pyramid_genshi import renderer_factory
    config.add_renderer('.genshi', renderer_factory)

def main(global_config, **settings):
    '''Configures and returns the Pyramid WSGI application.'''
    db_string = settings.get('db_string')
    if db_string is None:
        raise ValueError("No 'db_string' value in application configuration.")
    db_echo = settings.get('db_echo', 'false')
    initialize_sql(db_string, asbool(db_echo))
    # Every installation of FormCreator should have its own salt (a string)
    # for creating user passwords hashes, so:
    from formcreator.models.auth import User
    User.salt = settings.pop('auth.password.hash.salt') # required config
    # Create and use *config*, a temporary wrapper of the registry.
    config = Configurator(**config_dict(settings))
    config.scan('formcreator')
    # enable_kajiki(config)
    enable_genshi(config)
    add_routes(config)
    return config.make_wsgi_app() # commits configuration (does some tests)
