#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import unittest as u  # http://docs.python.org/library/unittest.html
import colander as c
from mootiro_form.models.field import Field
from mootiro_form.fieldtypes.text import TextField
# Testes da Lea em it3s.documentos/Documentação_Treinamento/Testing/


class TestEditTextField(u.TestCase):
    node = TextField.edit_schema

    def test_validate_default_value(self):
        '''Must reject the default value if outside bounds.'''
        dd = dict(enableLength=True, enableWords=True,
                  minLength='4', maxLength='21', minWords='2', maxWords='5')
        def d(val):
            dd['defaul'] = val
            return dd
        go = self.node.deserialize
        # These default values must validate OK
        go(d('Well within bounds'))
        go(d('Five words is our max'))
        go(d('1 34'))
        go(d(''))
        # These must fail...
        must_fail = ['123', '1 3', '6 words at a pop bip',
            'Exactly 22 characters.']
        for defaul in must_fail:
            self.assertRaises(c.Invalid, go, d(defaul))
        # ...but the same values are OK if we turn off length validation
        dd['enableLength'] = False
        dd['enableWords'] = False
        for defaul in must_fail:
            go(d(defaul))

    def _assert_length_ok(self, min, max):
        self.node.deserialize(dict(minLength=min, maxLength=max,
            enableLength=True, enableWords=False))
        self.node.deserialize(dict(minLength=min, maxLength=max,
            enableLength=False, enableWords=False))
        self.node.deserialize(dict(minWords=min, maxWords=max,
            enableLength=False, enableWords=True))
        self.node.deserialize(dict(minWords=min, maxWords=max,
            enableLength=False, enableWords=False))

    def _assert_length_invalid(self, min, max):
        self.assertRaises(c.Invalid, self.node.deserialize,
            dict(minLength=min, maxLength=max,
                 enableLength=True, enableWords=False))
        self.assertRaises(c.Invalid, self.node.deserialize,
            dict(minLength=min, maxLength=max,
                 enableLength=False, enableWords=False))
        self.assertRaises(c.Invalid, self.node.deserialize,
            dict(minWords=min, maxWords=max,
                 enableLength=False, enableWords=True))
        self.assertRaises(c.Invalid, self.node.deserialize,
            dict(minWords=min, maxWords=max,
                 enableLength=False, enableWords=False))

    def test_validate_length(self):
        '''min and max length in themselves and in relation to each other.
        The other parameters shouldn't matter in this test.

        Uses the same data points to test min and max words, too.
        '''
        self._assert_length_ok(1, 99)
        self._assert_length_ok('1', '9')
        self._assert_length_invalid(2,  1)
        self._assert_length_invalid(0,  1)
        self._assert_length_invalid(0,  0)
        self._assert_length_invalid(-1, 1)
        self._assert_length_invalid('ha', 5)
        self._assert_length_invalid(4, 'bru')
        self._assert_length_invalid('1.', '5')
        self._assert_length_invalid('1', '5.')
        self._assert_length_invalid('1.5', '5')
        self._assert_length_invalid('1', '5.5')
        self._assert_length_invalid('3/2', '5')
        self._assert_length_invalid('3', '5/2')


if __name__ == '__main__':
    u.main()
