# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from formcreator.models import DBSession
from formcreator.models import MyModel

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
    return {'root':root, 'project':'formcreator'}
