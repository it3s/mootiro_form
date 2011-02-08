# -*- coding: utf-8 -*-
'''Our request decorations.'''

from __future__ import unicode_literals # unicode by default

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import authenticated_userid
from pyramid.url import route_url
from mootiro_form.models import User, sas
from mootiro_web.page_deps import DepsRegistry, PageDeps


def init_deps(settings):
    '''Declares all javascript and stylesheet dependencies.'''
    global deps
    deps = DepsRegistry(profiles='development|cdn|static',
                        profile=settings.get('page_deps.profile', 'cdn'))

    # The first URL is for development (uncompressed js, can be debugged)
    # The second URL is for production (Google CDN, fastest)
    # The third URL is for production (static, for when Google is out).
    deps.lib('jquery', ('http://' + settings['url_root'] + 'static/lib/jquery-1.5.js',\
        'https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js'))
        # also possible: /deform/scripts/jquery-1.4.2.min.js
    deps.lib('deform', 'http://' + settings['url_root'] + 'deform/scripts/deform.js', depends='jquery')
    deps.stylesheet('deform1', 'http://' + settings['url_root'] + 'deform/css/form.css')
    deps.stylesheet('deform2', 'http://' + settings['url_root'] + 'deform/css/theme.css')
    deps.package('deform', libs='deform', css='deform1|deform2',
                 onload='deform.load();')
    deps.lib('jquery.ui', ('http://' + settings['url_root'] + 'static/lib/jquery-ui-1.8.9.min.js',
        'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js',
        'http://' + settings['url_root'] + 'static/lib/jquery-ui-1.8.9.min.js'), depends='jquery')
    deps.stylesheet('jquery.ui', 'http://ajax.googleapis.com/ajax/libs/',\
                    'http://' + settings['url_root'] + 'jqueryui/1.8.8/themes/base/jquery-ui.css')
    deps.package('jquery.ui', libs='jquery.ui', css='jquery.ui')
    deps.lib('infieldlabel', 'http://' + settings['url_root'] + 'static/lib/jquery.infieldlabel.min.js',
             depends='jquery')
    deps.stylesheet('master_global', 'http://' + settings['url_root'] + 'static/css/master_global.css')
    deps.stylesheet('master_logged', 'http://' + settings['url_root'] + 'static/css/master_logged.css')
    deps.stylesheet('master_cover' , 'http://' + settings['url_root'] + 'static/css/master_cover.css')
    deps.stylesheet('form_edit'    , 'http://' + settings['url_root'] + 'static/css/form_edit.css')


class MyRequest(Request):
    def __init__(self, *a, **kw):
        super(MyRequest, self).__init__(*a, **kw)
        self.page_deps = PageDeps(deps)

    @reify
    def user(self):
        '''Memoized user object. If we always use request.user to retrieve
        the authenticated user, the query will happen only once per request,
        which is good for performance.
        '''
        userid = authenticated_userid(self)
        return sas.query(User).get(userid) if userid else None
