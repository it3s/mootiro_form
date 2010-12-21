# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config
from formcreator.models import DBSession

# @view_config(renderer='templates/root.mako')
def root(request):
    return render_to_response('root.mako', {})
    return dict(hello='world')
    return Response('Hello world, and hello Zeitgeist.')

''' Deprecated:
class RootView(object):
    def root(self, context, request):
        dbsession = DBSession()
        return Response('Hello world, and hello Zeitgeist.')
        return Response(dict(hello='world', context=context, request=request))
'''
