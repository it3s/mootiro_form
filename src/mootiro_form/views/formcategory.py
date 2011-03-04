# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, sas
from mootiro_form.views import BaseView, authenticated
from pyramid.response import Response
import json

class FormCategoryView(BaseView):
    ''' The form category edition view'''
   
    #user = self.request.user

    @action(name='view', request_method='GET')
    @authenticated
    def view(self):
        '''Displays all categories'''
        cat_id = self.request.matchdict.get('id')
        user = self.request.user

        if cat_id == 'all':
            categories = sas.query(FormCategory).\
                    filter(FormCategory.user==user).all()
            return Response(unicode(categories))
        else:
            category = sas.query(FormCategory)\
                    .filter(FormCategory.id==cat_id)\
                    .filter(FormCategory.user==user).one()
            return Response(unicode(category))
    
    
    @action(name='edit', renderer='JSON', request_method='POST')
    @authenticated
    def save(self):
        '''Creates or updates a Category from POSTed data if it validates;
        else displays error messages'''
        cat_id = self.request.matchdict.get('id')
        

    @action(renderer='json', request_method='POST')
    def rename(self):
        cat_id = self.request.matchdict['id']
        print cat_id
        cat_name = self.request.POST['category_name']
        print cat_name
        print "DEVERIA ter printado category_name"
        category = sas.query(FormCategory).filter(FormCategory.id==cat_id)\
                .one()
        if category:
            category.name = cat_name
            sas.flush()
            errors = ''
        else:
            errors = _("Error finding category")
            return {'errors': errors}

    @action(renderer='json', request_method='POST')
    @authenticated
    def delete(self):
        user = self.request.user
        cat_id = int(self.request.matchdict.get('id'))
        category = sas.query(FormCategory).filter(FormCategory.id == cat_id) \
            .filter(FormCategory.user==user).one()
        if category:
            sas.delete(category)
            sas.flush()
            errors = ''
        else:
            errors = _("This category does not exist!")
            if user.categories:
                categories_data = [cat.to_json() for cat in user.categories]
                
         
        return {'errors': errors, 'categories': categories_data}


