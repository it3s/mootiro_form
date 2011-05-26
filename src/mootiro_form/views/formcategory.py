# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Form, User, FormCategory, sas
from mootiro_form.views import BaseView, authenticated, d, get_button
from pyramid.response import Response
from mootiro_form.schemas.formcategory import create_category_schema

#new_category_schema = NewCategorySchema()

def new_category_form(user):
    return d.Form(create_category_schema(user), formid='newcategoryform')

class FormCategoryView(BaseView):
    ''' The form category edition view'''

    #user = self.request.user

    @action(name='edit', renderer='create_category.genshi',
            request_method='GET')
    @authenticated
    def display_edit_category_form(self):
        '''Displays the form to create a new category.'''
        id = self.request.matchdict.get('id')
        user = self.request.user
        if id == 'new':
            create_category_link = self.url('category', action='new', id=id)
            return dict(link=create_category_link,
                    new_category_form=new_category_form(user).render())

    @action(name='edit', renderer='json', request_method='POST')
    @authenticated
    def edit_category(self):
        '''Receives and validates POSTed data. If data is okay, creates the
        category. Otherwise, returns the form with errors.
        '''
        user = self.request.user
        controls = self.request.POST.items()
        try:
            appstruct = new_category_form(user).validate(controls)
        except d.ValidationFailure as e:
            self.request.override_renderer = 'create_category.genshi'
            return dict(pagetitle=_("New category"), new_category_form=e.render())
        user = self.request.user
        cat_name = appstruct['name']
        cat_desc = appstruct['description']
        if cat_name != '':
            category = sas.query(FormCategory) \
                    .filter(FormCategory.name==cat_name) \
                    .filter(FormCategory.user==user) \
                    .first()
        if category: #If the system found a category, doesn't create a new one
            errors = _("That category already exists.")
            return {'errors': errors}
        else: #Create a category!
            new_category = FormCategory(name=cat_name, description=cat_desc,
                                        user=user)
            sas.add(new_category)
            sas.flush()
            all_data = user.all_categories_and_forms()
            return dict(changed=True, all_data=all_data)


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
                categories_data = [cat.to_dict() for cat in user.categories]
        return {'errors': errors, 'categories': categories_data}
