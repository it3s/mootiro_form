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
    
    
    @action(name='new', renderer='JSON', request_method='POST')
    @authenticated
    def create(self):
        '''Creates a Category from POSTed data if it validates;
        else displays error messages'''
        #cat_id = self.request.matchdict.get('id')
        cat_name = self.request.POST['category_name']
        cat_description = self.request.POST['category_description']
        user = self.request.user
        if cat_name != '':
            category = sas.query(FormCategory).\
                    filter(FormCategory.name==cat_name).\
                    filter(FormCategory.user==user).\
                    first()
        if category: #If the system found a category, doesn't create a new one
            errors = _("Error finding category")
            return {'errors': errors}
        else: #Create a category!
            new_category = FormCategory(name=cat_name, description =
                    cat_description, user = user)
            sas.add(new_category)
            sas.flush()


    @action(renderer='json', request_method='POST')
    def rename(self):
        cat_id = self.request.matchdict['id']
        cat_name = self.request.POST['category_name']
        if cat_name != '':
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


