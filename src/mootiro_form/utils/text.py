# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import random


def random_word(wordLen):
    '''Returns a random string with worLen length'''
    word = ''
    for i in range(wordLen):
        word += random.choice(\
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%*()_')
    return word
