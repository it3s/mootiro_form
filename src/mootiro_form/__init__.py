# -*- coding: utf-8 -*-

'''Main configuration of MootiroForm.'''

from __future__ import unicode_literals  # unicode by default

__appname__ = 'MootiroForm'
package_name = 'mootiro_form'

import json
import os
import pyramid_handlers
from pyramid.resource import abspath_from_resource_spec
from pyramid.i18n import get_localizer
from mootiro_web.pyramid_starter import PyramidStarter, all_routes

from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory(package_name)
del TranslationStringFactory


def add_routes(config):
    '''Configures all the URLs in this application.'''
    config.add_static_view('static', 'mootiro_form:static')
    # The *Deform* form creation library uses this:
    config.add_static_view('deform', 'deform:static')
    # config.add_route('root', '', view=root.root, renderer='root.mako',)
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

    handler('image_preview', 'file/{action}/{id}',
            handler='mootiro_form.views.file.FileView')
    handler('file', 'file/{action}/{id}/{field}',
            handler='mootiro_form.views.file.FileView')

    # TODO 1. The order is wrong, should be form/id/action. Change and TEST
    handler('form', 'form/{action}/{id}',
            handler='mootiro_form.views.form.FormView')
    handler('form_template', 'form/template/{action}/{id}',
            handler='mootiro_form.views.formtemplate.FormTemplateView')
    handler('entry_form_slug_css', 'entry/{action}/s/{slug}/style.css',
            handler='mootiro_form.views.entry.EntryView')
    handler('entry_form_slug', 'entry/{action}/s/{slug}',
            handler='mootiro_form.views.entry.EntryView')
    handler('entry', 'entry/{action}/{id}',
            handler='mootiro_form.views.entry.EntryView')
    handler('entry_list', 'entry/{action}/{form_id}/{page}/{limit}',
            handler='mootiro_form.views.entry.EntryView')
    handler('email_validation', 'email_validation/{action}',
            handler='mootiro_form.views.user.UserView')
    handler('email_validator', 'email_validation/{action}/{key}',
            handler='mootiro_form.views.user.UserView')
    handler('category', 'category/{action}/{id}',
            handler='mootiro_form.views.formcategory.FormCategoryView')


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
    from pyramid_beaker import session_factory_from_settings
    import mootiro_form.request as mfr
    auth = auth_tuple()
    return dict(settings=settings,
                request_factory=mfr.MyRequest,
                session_factory=session_factory_from_settings(settings),
                authentication_policy=auth[0],
                authorization_policy=auth[1],
    )


def configure_upload(settings, ps):
    from .fieldtypes.image import ImageField
    from .fieldtypes.file import TempStore, tmpstore

    upload_data_dir = settings.get('upload.data_dir', '{up}/data/uploads')
    upload_temp_dir = settings.get('upload.temp_dir', '{up}/data/uploads/temp')

    ImageField.upload_data_dir = upload_data_dir
    TempStore.upload_temp_dir = upload_temp_dir

    ps.makedirs(upload_data_dir)
    ps.makedirs(upload_temp_dir)


def main(global_config, **settings):
    '''Configures and returns the Pyramid WSGI application.'''
    from mootiro_web.pyramid_deform import monkeypatch_colander
    monkeypatch_colander()

    ps = PyramidStarter(package_name, __file__, settings,
        config_dict(settings), require_python27=True)
    ps._ = _
    ps.enable_turbomail()
    ps.configure_favicon()

    # Every installation of MootiroForm should have its own salt (a string)
    # for creating user passwords hashes, so:
    from .models.user import User
    User.salt = settings.pop('auth.password.hash.salt')  # required config
    ps.makedirs(settings.get('dir_data', '{up}/data'))
    # ...and now we can...
    ps.enable_sqlalchemy()

    # This is global because it is required in schema/user.py
    global enabled_locales
    # Turn a space-separated list into a list, for quicker use later
    locales_filter = settings['enabled_locales'] = \
        settings.get('enabled_locales', 'en').split(' ')
    # This list always has to be updated when a new language is supported
    supported_locales = [dict(name='en', title='Change to English'),
                     dict(name='en_DEV', title='Change to dev slang'),
                     dict(name='pt_BR', title='Mudar para português'),
                     dict(name='es', title='Cambiar a español'),
                     dict(name='de', title='Zu Deutsch wechseln')]
    enabled_locales = []
    for locale in locales_filter:
        for adict in supported_locales:
            if locale == adict['name']:
                enabled_locales.append(adict)
    import views
    views.enabled_locales = enabled_locales

    ps.enable_internationalization(extra_translation_dirs= \
        ('deform:locale', 'colander:locale'))
    ps.enable_genshi()

    if settings.get('CAS.enable', False) == 'true':
        from mootiro_web.pyramid_auth import CasAuthenticator
        ps.set_authenticator(CasAuthenticator(ps.settings))
    else:
        from mootiro_form.views.user import LocalAuthenticator
        ps.set_authenticator(LocalAuthenticator(ps.settings))

    configure_upload(settings, ps)

    ps.enable_handlers()
    add_routes(ps.config)

    import mootiro_form.request as mfr
    mfr.init_deps(settings)

    #Pyramid 1.2: config.make_wsgi_app should be called before config.get_routes_mapper().get_routes
    r =  ps.result()  # commits configuration (does some tests)

    base_path = settings.get('base_path', '/')
    create_urls_js(ps.config, settings, base_path)
    global routes_json
    routes_json = create_urls_json(ps.config, base_path)

    return r
