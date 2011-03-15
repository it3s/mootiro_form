# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

import json

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid_handlers import action
from turbomail import Message
from mootiro_form.views import BaseView, d
from mootiro_form.utils import create_locale_cookie
from mootiro_form.models import Form, FormCategory, sas
from mootiro_form.schemas.contact import Contact


class Root(BaseView):
    '''The front page of the website.'''

    @action(renderer='root.genshi')
    def root(self):
        if self.request.user:
            self.request.override_renderer = 'logged_root.genshi'
            return self.logged_root()
        else:
            return dict()

    def logged_root(self):
        user = self.request.user
        all_data = user.all_categories_and_forms_in_json()
        print all_data
        return dict(all_data=all_data)
        

    @action(renderer='noscript.genshi')
    def noscript(self):
        return dict()

    @action()
    def favicon(self):
        settings = self.request.registry.settings
        icon = open(settings['favicon'], 'r')
        return Response(content_type=settings['favicon_content_type'],
                        app_iter=icon)

    @action()
    def locale(self):
        '''Sets the locale cookie and redirects back to the referer page.'''
        location = self.request.referrer
        if not location:
            location = '/'
        locale = self.request.matchdict['locale']
        settings = self.request.registry.settings
        headers = create_locale_cookie(locale, settings)
        return HTTPFound(location=location, headers=headers)

    @action(name='contact', renderer='contact.genshi', request_method='GET')
    def show_contact_form(self):
        '''Displays the contact form'''
        contact_form_schema = Contact() # Initializing the contact form schema
        # "action" defines where the form POSTs to
        contact_form = d.Form(contact_form_schema, buttons=('submit',),
            action=self.url('contact'), formid='contactform') 
        return dict(pagetitle="Contact Form",
                    contact_form=contact_form.render())

    @action(name='contact', renderer='contact.genshi', request_method='POST')
    def save_contact_form(self):
        '''Sends the form for sending contact emails if POSTed data validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        try:
            contact_form_schema = Contact()
            appstruct = d.Form(contact_form_schema, buttons=('submit',),
                    action=self.url('contact'),
                    formid='contactform').validate(controls) 
        # If form does not validate, returns the form
        except d.ValidationFailure as e:
            return dict(pagetitle="Contact Form", contact_form=e.render())
        # Form validation passes, so send the e-mail
        msg = Message(author=(appstruct['name'], appstruct['email']),
            subject=appstruct['subject'], plain=appstruct['message'])
        msg.send()
        self.request.override_renderer = 'contact_successful.genshi'
        return dict()
