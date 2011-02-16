# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, sas
from mootiro_form.views import BaseView, authenticated
from pyramid.response import Response

class FormCategoryView(BaseView):
    ''' The form category edition view'''
    
    @action(name='view', request_method='GET')
    @authenticated
    def view(self):
        '''Displays all categories'''
        cat_id = self.request.matchdict.get('id')
        if cat_id == 'all':
            categories = sas.query(FormCategory).all()
            return Response(unicode(categories))
        else:
            category = sas.query(FormCategory)\
                    .filter(FormCategory.id==cat_id).one()
            return Response(unicode(category))
        
    @action(name='delete', request_method='GET')
    @authenticated
    def delete(self):
        '''Removes one category'''
        cat_id = self.request.matchdict.get('id')
        category = sas.query(FormCategory)\
                .filter(FormCategory.id==cat_id).one()
        sas.delete(category)
        return Response("Should be done")

    @action(name='update', request_method='POST')
    @authenticated
    def update(self):
        pass



