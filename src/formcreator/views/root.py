# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid import Response
from formcreator.models import DBSession

class RootView(object):
    def root(self, context, request):
        dbsession = DBSession()
        return Response(hello='world', context=context, request=request)
