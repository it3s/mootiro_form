# -*- coding: utf-8 -*-

'''Main configuration of MootiroForm.'''

from __future__ import unicode_literals  # unicode by default

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
    # Our custom request class uses PageDeps:
    from mootiro_form.deps import init_deps
    deps = init_deps(settings)
    from mootiro_web.user import get_request_class
    MootiroRequest = get_request_class(deps, settings)

    auth = auth_tuple()
    from pyramid_beaker import session_factory_from_settings
    return dict(settings=settings,
                request_factory=MootiroRequest,
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
    ps.enable_handlers()
    from mootiro_web.user import enable_auth
    enable_auth(ps.settings, ps.config)
    ps.enable_turbomail()
    ps.configure_favicon()
    ps.makedirs(settings.get('dir_data', '{up}/data'))
    # ...and now we can...
    ps.enable_sqlalchemy()

    ps.enable_internationalization(extra_translation_dirs= \
        ('deform:locale', 'colander:locale'))

    ps.enable_deform(['mootiro_form:fieldtypes/templates', 'deform:templates'])
    ps.set_template_globals()

    configure_upload(settings, ps)

    ps.enable_handlers()
    add_routes(ps.config)
    ps.enable_genshi()

    #Pyramid 1.2: config.make_wsgi_app should be called before config.get_routes_mapper().get_routes
    r =  ps.result()  # commits configuration (does some tests)

    base_path = settings.get('base_path', '/')
    create_urls_js(ps.config, ps.settings, base_path)
    global routes_json
    routes_json = create_urls_json(ps.config, base_path)

    return r
