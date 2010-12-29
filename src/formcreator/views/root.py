# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config
from formcreator.models import User, sas
from pyramid.security import authenticated_userid
from mako import exceptions

def root(request):
    userid = authenticated_userid(request)
    if userid is None:
        print('Not authenticated.')
        user = None
    else:
        user = sas.query(User).get(userid)
        print(user)
    '''
    try:
        render_to_response('root.mako', {})
    except Exception as e:
        return Response(exceptions.text_error_template().render())
    '''    
    return dict(user=user)
