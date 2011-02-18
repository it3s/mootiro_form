# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

def create_locale_cookie(locale, settings):
        '''Ceates the locale cookie; Is used in user view in update_user() and
        authenticate()'''
        if locale in settings['enabled_locales']:
            headers = [('Set-Cookie',
                '_LOCALE_={0}; expires=31 Dec 2050 23:00:00 GMT; Path=/' \
                .format(locale))]
        else:
            headers = None
        return headers


