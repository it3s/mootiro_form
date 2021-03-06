# -*- coding: utf-8 -*-
'''Our request decorations.'''

from __future__ import unicode_literals  # unicode by default


def init_deps(settings):
    '''Declares all javascript and stylesheet dependencies.'''
    from mootiro_web.page_deps import DepsRegistry
    deps = DepsRegistry(profiles='development|cdn|static',
                        profile=settings.get('page_deps.profile', 'cdn'))
    rooted = lambda(path): settings.get('base_path', '/') + path

    # The first URL is for development (uncompressed js, can be debugged)
    # The second URL is for production (Google CDN, fastest)
    # The third URL is for production (static, for when Google is out).
    deps.lib('jquery', (rooted('static/lib/jquery-1.5.2.js'),
        'http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js',
        '/static/lib/jquery-1.5.2.min.js'))
        # also possible: /deform/scripts/jquery-1.4.2.min.js
    deps.lib('deform', rooted('deform/scripts/deform.js'), depends='jquery')
    deps.stylesheet('deform1', rooted('deform/css/form.css'))
    deps.package('deform', css='deform1',  # css='deform1|deform2',
                 libs='deform', onload='deform.load();')
    deps.lib('jquery.ui', (rooted('static/lib/jquery-ui-1.8.11.custom.min.js'),
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/jquery-ui.min.js',
        rooted('static/lib/jquery-ui-1.8.11.custom.min.js')), depends='jquery')
    deps.stylesheet('jquery.ui', (rooted('static/css/custom-theme/jquery-ui-1.8.11.custom.css'),
        'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.11/themes/' \
        'base/jquery-ui.css', rooted('static/css/custom-theme/jquery-ui-1.8.11.custom.css')))
    deps.package('jquery.ui', libs='jquery.ui', css='jquery.ui')
    deps.lib('global', rooted('static/js/global.js'))
    deps.lib('validators', rooted('static/js/validators.js'))
    deps.lib('infieldlabel', rooted('static/lib/jquery.infieldlabel.min.js'),
             depends='jquery')
    deps.lib('jquery-json', rooted('static/lib/jquery.json-2.2.min.js'),
             depends='jquery')
    deps.lib('datetimepicker', rooted('static/lib/datetimepicker.js'),
             depends='jquery.ui')
    deps.lib('date', rooted('static/lib/date.js'))
    deps.lib('js_url', rooted('static/js/url.js'))
    deps.lib('form_entry', rooted('static/js/form_entry.js'), depends='js_url')
    deps.stylesheet('master_global', rooted('static/css/master_global.css'))
    deps.stylesheet('collectors', rooted('static/css/collectors.css'))
    deps.stylesheet('master_logged', rooted('static/css/master_logged.css'))
    deps.stylesheet('master_cover',  rooted('static/css/master_cover.css'))
    deps.stylesheet('list', rooted('static/css/list.css'))
    deps.stylesheet('forms_list', rooted('static/css/forms_list.css'))
    deps.stylesheet('form_answers', rooted('static/css/form_answers.css'))
    deps.stylesheet('form_edit',     rooted('static/css/form_edit.css'))
    deps.stylesheet('entry_creation', rooted('static/css/entry_creation.css'))
    deps.lib('jquery.tmpl', (rooted('static/lib/jquery.tmpl.js'),
             'http://ajax.microsoft.com/ajax/jquery.templates/beta1/jquery.tmpl.min.js',
             rooted('static/lib/jquery.tmpl.min.js')),
             depends='jquery')
    deps.lib('ListField', rooted('static/fieldtypes/ListField/list_entry.js'),
             depends='jquery')
    deps.lib('ImageField', rooted('static/fieldtypes/ImageField/image_entry.js'),
             depends='jquery')
    deps.lib('Entry', rooted('static/js/entry.js'),
             depends='jquery')
    deps.lib('TinyMCE', rooted('static/lib/tiny_mce/tiny_mce.js'),
             depends='jquery')
    deps.lib('rich_editor', rooted('static/js/rich_editor.js'),
             depends='TinyMCE')
    return deps
