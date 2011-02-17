# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
from mootiro_form.views import static_url


class FieldType(object):
    '''Base class for field types.

    Every subclass must implement:

    - a `name` string
    - a `brief` description string
    
    '''
    def script_url(self, request):
        return static_url('mootiro_form:static/fieldtypes/{}/editing.js' \
            .format(type(self).__name__), request)
    
    def icon_url(self, request):
        return static_url('mootiro_form:static/fieldtypes/{}/icon.png' \
            .format(type(self).__name__), request)


from mootiro_form.fieldtypes.line import LineField

all_fieldtypes = [LineField()]
