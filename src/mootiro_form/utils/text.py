# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import random


def random_word(length, chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                              'abcdefghijklmnopqrstuvwxyz' \
                              '0123456789!@$%*()_'):
    '''Returns a random string with some `length`.'''
    """
    alist = []
    for i in xrange(length):
        alist.append(random.choice(chars))
    return ''.join(alist)
    """
    return ''.join((random.choice(chars) for i in xrange(length)))
