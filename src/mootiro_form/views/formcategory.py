# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, sas
from mootiro_form.views import BaseView, authenticated, d, get_button
from pyramid.response import Response
from mootiro_form.schemas.formcategory import NewCategorySchema
import json

new_category_schema = NewCategorySchema()

def new_category_form(button=_('submit'), action=''):
    '''Apparently, Deform forms must be instantiated for every request.'''
    return d.Form(new_category_schema, buttons=(get_button(button),),
                  action=action, formid='newcategoryform')

def update_new_category_form():
    return d.Form(new_category_schema, formid='newcategoryform')

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
    
    
    @action(name='edit', renderer='create_category.genshi',
            request_method='GET')
    @authenticated
    def display_edit_category_form(self):
        '''Displays the form to create a new category.'''
        if self.request.matchdict.get('id') == 'new':
            id = self.request.matchdict.get('id')
            create_category_link = self.url('category', action='new', id=id)
            return dict(pagetitle="New Category", link=create_category_link,
                    new_category_form = new_category_form().render())


    @action(name='edit', renderer='json', request_method='POST') 
    @authenticated
    def edit_category(self):
        '''Receives and validates POSTed data. If data is okay, creates the
        category. Otherwise, returns the form with errors.
        '''
        controls = self.request.POST.items()
        print controls
        try:
            appstruct = update_new_category_form().validate(controls)
            print "Passou pelo try appstruct"
        except d.ValidationFailure as e:
            print "entrou no except d.ValidationFailure"
            self.request.override_renderer = 'create_category.genshi'
            return dict(pagetitle="New Category", new_category_form=e.render())
        #Form validation passes, so insert the category in the database!
        print "Entrou no codigo de incluir categoria"
        user = self.request.user
        cat_name = appstruct['category_name']
        cat_description = appstruct['category_description']
        if cat_name != '':
            category = sas.query(FormCategory).\
                    filter(FormCategory.name==cat_name).\
                    filter(FormCategory.user==user).\
                    first()
        if category: #If the system found a category, doesn't create a new one
            errors = _("Error finding category")
            return {'errors': errors}
        else: #Create a category!
            new_category = FormCategory(name=cat_name, description=
                    cat_description, user=user)
            sas.add(new_category)
            sas.flush()
            return dict(changed=True)


    @action(renderer='json', request_method='POST')
    def rename(self):
        cat_id = self.request.matchdict.get('id')
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


