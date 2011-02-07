# -*- coding: utf-8 -*-
'''Our request decorations.'''

from __future__ import unicode_literals # unicode by default

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import authenticated_userid
from mootiro_form.models import User, sas
from mootiro_web.page_deps import DepsRegistry, PageDeps


x3 = lambda url: (url, url, url)

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
    deps.lib('deform', x3('/deform/scripts/deform.js'), depends='jquery')
    deps.stylesheet('deform1', x3('/deform/css/form.css'))
    deps.stylesheet('deform2', x3('/deform/css/theme.css'))
    deps.package('deform', libs='deform', css='deform1|deform2')
    deps.lib('jquery.ui', ('/static/js/jquery-ui.js',
        'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js',
        '/static/js/jquery-ui-1.8.9.custom.min.js'), depends='jquery')
    deps.stylesheet('master_global', x3('/static/css/master_global.css'))
    deps.stylesheet('master_cover', x3('/static/css/master_cover.css'))
    deps.lib('infieldlabel', x3('/static/js/jquery.infieldlabel.min.js'),
             depends='jquery.ui')


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
