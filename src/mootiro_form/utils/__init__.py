# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default


def create_locale_cookie(locale, settings):
    '''Creates the locale cookie; used in user view in update_user(),
    save_user() and authenticate().
    '''
    if locale in settings['enabled_locales']:
        headers = [(b'Set-Cookie',
            b'_LOCALE_={0}; expires=Fri, 31-Dec-9999 23:00:00 GMT; Path=/' \
            .format(locale.encode('utf8')))]
    else:
        headers = None
    return headers
