# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action

from mootiro_form import _
from mootiro_form.models import User, Form, sas
from mootiro_form.views import BaseView, authenticated


class FormView(BaseView):
    """The form editing view."""
    CREATE_TITLE = _('New form')
    EDIT_TITLE = _('Edit form')

    @action(name='new', renderer='form_edit.genshi', request_method='GET')
    @authenticated
    def new_form(self):
        '''Displays a new form, ready for editing.'''
        return dict(pagetitle=self.CREATE_TITLE, form=Form())

    @action(name='new', renderer='form_edit.genshi', request_method='POST')
    @authenticated
    def create(self):
        '''Creates a new Form from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        try:
            appstruct = user_form().validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.CREATE_TITLE, user_form = e.render())
        # Form validation passes, so create a User in the database.
        u = User(**appstruct)
        sas.add(u)
        sas.flush()
        return self.authenticate(u.id)

    @action(renderer='form_edit.genshi', request_method='GET')
    def edit(self):
        '''Displays the form editor, for an existing form.'''
        user = self.request.user
        return dict(pagetitle=self.EDIT_TITLE,
            user_form=user_form().render(self.model_to_dict(user,
                ('nickname', 'real_name', 'email', 'password'))))
