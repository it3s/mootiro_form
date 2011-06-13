# -*- coding: utf-8 -*-

'''Main configuration of MootiroForm.'''

from __future__ import unicode_literals  # unicode by default

__appname__ = 'MootiroForm'
package_name = 'mootiro_form'

# Demand Python 2.7 (I want to be sure I am not trying to run it on 2.6.)
from sys import version_info, exit
version_info = version_info[:2]
if version_info < (2, 7) or version_info >= (3, 0):
    exit('\n' + __appname__ + ' requires Python 2.7.x.')
del version_info, exit


import json
import os
from mimetypes import guess_type

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory(package_name)

import pyramid_handlers

from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from pyramid.resource import abspath_from_resource_spec
from pyramid.i18n import get_localizer

import mootiro_form.request as mfr


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
    handler('contact', 'contact',
            handler='mootiro_form.views.root.Root', action='contact')
    handler('user', 'user/{action}',
            handler='mootiro_form.views.user.UserView')
    handler('reset_password', 'user/{action}/{slug}',
            handler='mootiro_form.views.user.UserView')

    handler('collectors', 'form/{id}/collectors', action='collectors',
            handler='mootiro_form.views.collector.CollectorView')
    handler('collector', 'form/{form_id}/collector/{id}/{action}',
            handler='mootiro_form.views.collector.CollectorView')
    handler('collector_slug', 'collector/{action}/s/{slug}',
            handler='mootiro_form.views.collector.CollectorView')
    handler('form_no_id', 'form/{action}',
            handler='mootiro_form.views.form.FormView'),
    # TODO 1. The order is wrong, should be form/id/action. Change and TEST
    handler('form', 'form/{action}/{id}',
            handler='mootiro_form.views.form.FormView')
    handler('form_template', 'form/template/{action}/{id}',
            handler='mootiro_form.views.formtemplate.FormTemplateView')
    handler('entry', 'entry/{action}/{id}',
            handler='mootiro_form.views.entry.EntryView')
    handler('entry_list', 'entry/{action}/{id}/{page}/{limit}',
            handler='mootiro_form.views.entry.EntryView')
    # TODO change the views under this route to be under the collector_slug
    #      there is no need to have two slugged routes
    # the slug is for creating entries
    handler('entry_form_slug', 'entry/{action}/s/{slug}',
            handler='mootiro_form.views.entry.EntryView')
    handler('entry_form_slug_css', 'entry/{action}/s/{slug}/style.css',
            handler='mootiro_form.views.entry.EntryView')
    handler('email_validation', 'email_validation/{action}',
            handler='mootiro_form.views.user.UserView')
    handler('email_validator', 'email_validation/{action}/{key}',
            handler='mootiro_form.views.user.UserView')
    handler('category', 'category/{action}/{id}',
            handler='mootiro_form.views.formcategory.FormCategoryView')


def all_routes(config):
    '''Returns a list of the routes configured in this application.'''
    return [(x.name, x.pattern) for x in \
            config.get_routes_mapper().get_routes()]


def create_urls_json(config, base_path):
    routes_json = {}
    routes = all_routes(config)
    for handler, route in routes:
        if handler.endswith('/'):
            handler = handler[:-1]
        if route.endswith("/*subpath"):
            route = route[:-9]
        routes_json[handler] = base_path + route
    return json.dumps(routes_json)


def create_urls_js(config, settings, base_path):
    # TODO Check for errors
    here = os.path.abspath(os.path.dirname(__file__))  # src/mootiro_form/
    with open(here + '/utils/url.tpl.js', 'r') as js_template:
        js = js_template.read()
    with open(here + '/static/js/url.js', 'w') as new_js:
        new_js.write(js % (create_urls_json(config, base_path),
                           settings.get('scheme_domain_port', '')))


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
    return (AuthTktAuthenticationPolicy(
        'WeLoveCarlSagan', callback=find_groups, include_ip=True,
        timeout=60 * 60 * 3, reissue_time=60),
        None)  # ACLAuthorizationPolicy())


def config_dict(settings):
    '''Returns the Configurator parameters.'''
    auth = auth_tuple()
    return dict(settings=settings,
                request_factory=mfr.MyRequest,
                session_factory=session_factory_from_settings(settings),
                authentication_policy=auth[0],
                authorization_policy=auth[1],
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
    from mootiro_form.models import initialize_sql
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine, settings=settings)


def start_turbomail(settings):
    from turbomail.control import interface
    import atexit  # Necessary for the turbomail cleanup function
    options = dict((key, settings[key])
                    for key in settings
                    if key.startswith('mail.'))
    interface.start(options)
    atexit.register(interface.stop, options)


def mkdir(key):
    import os
    here = os.path.abspath(os.path.dirname(__file__))  # src/mootiro_form/
    up = os.path.dirname(here)                         # src/
    try:
        os.mkdir(key.format(here=here, up=up))
    except OSError:
        pass  # no problem, directory already exists


def main(global_config, **settings):
    '''Configures and returns the Pyramid WSGI application.'''
    mkdir(settings.get('dir_data', '{up}/data'))
    settings.setdefault('genshi.translation_domain', package_name)
    # needs to be global because is required in schema/user.py
    global enabled_locales
    # Turn a space-separated list into a list, for quicker use later
    locales_filter = settings['enabled_locales'] = \
        settings.get('enabled_locales', 'en').split(' ')
    # This list alwayys has to be updated when a new language is supported
    supported_locales = [dict(name='en', title='Change to English'),
                         dict(name='en_DEV', title='Change to dev slang'),
                         dict(name='pt_BR', title='Mudar para português')]
    enabled_locales = []
    for locale in locales_filter:
        for adict in supported_locales:
            if locale == adict['name']:
                enabled_locales.append(adict)
    import views
    views.enabled_locales = enabled_locales
    # Every installation of MootiroForm should have its own salt (a string)
    # for creating user passwords hashes, so:
    from .models.user import User
    User.salt = settings.pop('auth.password.hash.salt')  # required config
    # ...and now we can...
    start_sqlalchemy(settings)
    configure_favicon(settings)
    mfr.init_deps(settings)
    start_turbomail(settings)
    # Create and use *config*, a temporary wrapper of the registry.
    config = Configurator(**config_dict(settings))
    config.scan(package_name)

    # Enable i18n
    mkdir(settings.get('dir_locale', '{here}/locale'))
    config.add_translation_dirs(package_name + ':locale',
                                'deform:locale', 'colander:locale')
    #from pyramid.i18n import default_locale_negotiator
    #config.set_locale_negotiator(default_locale_negotiator)

    # Enable a nice, XML-based templating language
    # enable_kajiki(config)
    enable_genshi(config)

    add_routes(config)
    base_path = settings.get('base_path', '/')
    create_urls_js(config, settings, base_path)
    global routes_json
    routes_json = create_urls_json(config, base_path)
    return config.make_wsgi_app()  # commits configuration (does some tests)
