# -*- coding: utf-8 -*-
'''Our request decorations.'''

from __future__ import unicode_literals  # unicode by default

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import authenticated_userid

from mootiro_form.models import User, sas
from mootiro_web.page_deps import DepsRegistry, PageDeps


def init_deps(settings):
    '''Declares all javascript and stylesheet dependencies.'''
    rooted = lambda(path): settings['url_root'] + path
    global deps

    deps = DepsRegistry(profiles='development|cdn|static',
                        profile=settings.get('page_deps.profile', 'cdn'))

    # The first URL is for development (uncompressed js, can be debugged)
    # The second URL is for production (Google CDN, fastest)
    # The third URL is for production (static, for when Google is out).
    deps.lib('jquery', (rooted('static/lib/jquery-1.5.1.js'),
        'http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js',
        '/static/lib/jquery-1.5.1.min.js'))
        # also possible: /deform/scripts/jquery-1.4.2.min.js
    deps.lib('deform', rooted('deform/scripts/deform.js'), depends='jquery')
    deps.stylesheet('deform1', rooted('deform/css/form.css'))
    deps.stylesheet('deform2', rooted('deform/css/theme.css'))
    deps.package('deform', libs='deform', css='deform1|deform2',
                 onload='deform.load();')
    deps.lib('jquery.ui', (rooted('static/lib/jquery-ui-1.8.11.custom.min.js'),
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js',
        rooted('static/lib/jquery-ui-1.8.11.custom.min.js')), depends='jquery')
    deps.stylesheet('jquery.ui', (rooted('static/css/custom-theme/jquery-ui-1.8.11.custom.css'),
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/themes/' \
        'base/jquery-ui.css', rooted('static/css/custom-theme/jquery-ui-1.8.11.custom.css')))
    deps.package('jquery.ui', libs='jquery.ui', css='jquery.ui')
    deps.lib('infieldlabel', rooted('static/lib/jquery.infieldlabel.min.js'),
             depends='jquery')
    deps.lib('jquery-json', rooted('static/lib/jquery.json-2.2.min.js'),
             depends='jquery')
    deps.lib('datetimepicker', rooted('static/lib/datetimepicker.js'),
             depends='jquery.ui')
    deps.lib('date', rooted('static/lib/date.js'))
    deps.lib('js_url', rooted('static/js/url.js'))
    deps.lib('forms_list', rooted('static/js/forms_list.js'))
    deps.lib('form_entry', rooted('static/js/form_entry.js'))
    deps.stylesheet('master_global', rooted('static/css/master_global.css'))
    deps.stylesheet('master_logged', rooted('static/css/master_logged.css'))
    deps.stylesheet('master_cover',  rooted('static/css/master_cover.css'))
    deps.stylesheet('forms_list', rooted('static/css/forms_list.css'))
    deps.stylesheet('form_answers', rooted('static/css/form_answers.css'))
    deps.stylesheet('form_edit',     rooted('static/css/form_edit.css'))
    deps.stylesheet('entry_creation', rooted('static/css/entry_creation.css'))
    deps.stylesheet('ftemplate', rooted('static/css/form_templates/default.css'))
    deps.lib('jquery.tmpl', (rooted('static/lib/jquery.tmpl.js'),
             'http://ajax.microsoft.com/ajax/jquery.templates/beta1/jquery.tmpl.min.js',
             rooted('static/lib/jquery.tmpl.min.js')),
             depends='jquery')
    deps.lib('qsort', rooted('static/lib/qsort.min.js'),
             depends='jquery')
    deps.lib('ListField', rooted('static/fieldtypes/ListField/list_entry.js'),
             depends='jquery')
    deps.lib('Entry', rooted('static/js/entry.js'),
             depends='jquery')

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
