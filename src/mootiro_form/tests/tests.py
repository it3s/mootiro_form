# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import unittest

from pyramid.config import Configurator
from pyramid import testing


def _initTestingDB():
    from mootiro_form.models import initialize_sql
    session = initialize_sql('sqlite://')
    return session

'''
class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()  # should we use autocommit=True here?
        self.config.begin()
        _initTestingDB()

    def tearDown(self):
        self.config.end()

    def test_it(self):
        from mootiro_form.views import my_view  # doesn't exist anymore.
        # TODO: Write real tests :)
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['root'].name, 'root')
        self.assertEqual(info['project'], 'mootiro_form')
'''
