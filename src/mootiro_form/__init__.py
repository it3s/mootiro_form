# -*- coding: utf-8 -*-
'''Main configuration of Mootiro Form.'''

from __future__ import unicode_literals # unicode by default
from mimetypes import guess_type

__appname__ = 'Mootiro Form'
package_name = 'mootiro_form'

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory(package_name)

import pyramid_handlers

from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid_beaker import session_factory_from_settings
from pyramid.resource import abspath_from_resource_spec
from .views import MyRequest

def add_routes(config):
    '''Configures all the URLs in this application.'''
    config.add_static_view('static', 'mootiro_form:static')
    # The *Deform* form creation library uses this:
    config.add_static_view('deform', 'deform:static')
    # config.add_route('root', '', view=root.root, renderer='root.mako',)
    config.include(pyramid_handlers.includeme)
    # The above sets up pyramid_handlers, so now we can use:
    handler = config.add_handler
    handler('root', '',
            handler='mootiro_form.views.root.Root', action='root')
    handler('favicon', 'favicon.ico',
            handler='mootiro_form.views.root.Root', action='favicon')
    handler('noscript', 'noscript',
            handler='mootiro_form.views.root.Root', action='noscript')
    handler('locale', 'locale/{locale}',
            handler='mootiro_form.views.root.Root', action='locale')
    handler('user', 'user/{action}',
            handler='mootiro_form.views.user.UserView')
    handler('form_edit', 'form/{action}',
            handler='mootiro_form.views.form.FormView')

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
        ('WeLoveCarlSagan', callback=find_groups, include_ip=True,
         timeout=60*60*3, reissue_time=60),
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
    from mootiro_web.pyramid_kajiki import renderer_factory
    for extension in ('.txt', '.xml', '.html', '.html5'):
        config.add_renderer(extension, renderer_factory)

def enable_genshi(config):
    '''Allows us to use the Genshi templating language.
    We intend to switch to Kajiki down the road, therefore it would be best to
    avoid py:match.
    '''
    from mootiro_web.pyramid_genshi import renderer_factory
    config.add_renderer('.genshi', renderer_factory)

def configure_favicon(settings):
    settings['favicon'] = path = abspath_from_resource_spec(
        settings.get('favicon', 'mootiro_form:static/icon/32.png'))
    settings['favicon_content_type'] = guess_type(path)[0]

def start_sqlalchemy(settings):
    from sqlalchemy import engine_from_config
    from .models import initialize_sql
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine, settings=settings)

def mkdir(key):
    import os
    here = os.path.abspath(os.path.dirname(__file__)) # src/mootiro_form/
    up = os.path.dirname(here)                        # src/
    try:
        os.mkdir(key.format(here=here, up=up))
    except OSError:
        pass # no problem, directory already exists

def main(global_config, **settings):
    '''Configures and returns the Pyramid WSGI application.'''
    mkdir(settings.get('dir_data',   '{up}/data'))
    settings.setdefault('genshi.translation_domain', package_name)
    # Turn a space-separated list into a list, for quicker use later
    locales = settings.get('enabled_locales', 'en')
    settings['enabled_locales'] = locales.split(' ')
    # Every installation of Mootiro Form should have its own salt (a string)
    # for creating user passwords hashes, so:
    from .models.user import User
    User.salt = settings.pop('auth.password.hash.salt') # required config
    # ...and now we can...
    start_sqlalchemy(settings)
    configure_favicon(settings)
    # Create and use *config*, a temporary wrapper of the registry.
    config = Configurator(**config_dict(settings))
    config.scan(package_name)

    # Enable i18n
    mkdir(settings.get('dir_locale', '{here}/locale'))
    config.add_translation_dirs(package_name + ':locale/')
    #from pyramid.i18n import default_locale_negotiator
    #config.set_locale_negotiator(default_locale_negotiator)

    # Enable a nice, XML-based templating language
    # enable_kajiki(config)
    enable_genshi(config)

    add_routes(config)
    return config.make_wsgi_app() # commits configuration (does some tests)
