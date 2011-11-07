#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import *

def users_to_csv(filename):
    '''Usage:

    $ ./shell.sh
    from mootiro_form.utils.user_list import users_to_csv
    users_to_csv('/tmp/form-users.csv')
    # Locally:
    scp mootiro_form@form.mootiro.org:/tmp/form-users.csv .
    '''
    from bag.csv import CsvWriter
    print('Writing users to ' + filename)
    w = CsvWriter(file=open(filename, 'w'))
    w.put(['nickname', 'name', 'email', 'is_email_validated', 'password',
        'created', 'default_locale'])
    for user in sas.query(User):
        w.put([user.nickname, user.real_name, user.email,
            '1' if user.is_email_validated else '0',
            user.password_hash, user.created, user.default_locale])
    w.close()
    print('Done.')
