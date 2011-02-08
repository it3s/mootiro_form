# -*- coding: utf-8 -*-
'''Our request decorations.'''

from __future__ import unicode_literals # unicode by default

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import authenticated_userid
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
    deps.lib('jquery', ('/static/lib/jquery-1.5.js',
        'https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js',
        '/static/lib/jquery-1.5.min.js'))
        # also possible: /deform/scripts/jquery-1.4.2.min.js
    deps.lib('deform', '/deform/scripts/deform.js', depends='jquery')
    deps.stylesheet('deform1', '/deform/css/form.css')
    deps.stylesheet('deform2', '/deform/css/theme.css')
    deps.package('deform', libs='deform', css='deform1|deform2',
                 onload='deform.load();')
    deps.lib('jquery.ui', ('/static/lib/jquery-ui-1.8.9.min.js',
        'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js',
        '/static/lib/jquery-ui-1.8.9.min.js'), depends='jquery')
    deps.stylesheet('jquery.ui', 'http://ajax.googleapis.com/ajax/libs/' \
                    'jqueryui/1.8.8/themes/base/jquery-ui.css')
    deps.package('jquery.ui', libs='jquery.ui', css='jquery.ui')
    deps.lib('infieldlabel', '/static/lib/jquery.infieldlabel.min.js',
             depends='jquery')
    deps.stylesheet('master_global', '/static/css/master_global.css')
    deps.stylesheet('master_logged', '/static/css/master_logged.css')
    deps.stylesheet('master_cover' , '/static/css/master_cover.css')
    deps.stylesheet('form_edit'    , '/static/css/form_edit.css')


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
