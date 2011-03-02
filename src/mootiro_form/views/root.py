# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

import json

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid_handlers import action
from turbomail import Message
from mootiro_form.views import BaseView
from mootiro_form.utils import create_locale_cookie
from mootiro_form.models import Form, FormCategory, sas
import pprint

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
        '''Shows the contact form'''
        return dict()

    @action(name='contact', renderer='contact_successful.genshi',
            request_method='POST')
    def send_mail(self):
        '''Handles the form for sending contact emails.'''

        adict = self.request.POST

        name = adict['name']
        email = adict['email']
        subject = adict['subject']
        message = adict['message']

        #default_mail_sender = self.request.registry.settings['mail.default_dest']
        
        if email == "":
            return render_to_response('contact.genshi', {"name": name,
            "subject": subject, "message": message, "missing_email": True},
            request=self.request)
        

        #msg = Message(email, default_mail_sender, subject)
        msg = Message(author=(name, email), subject=subject, plain=message)
        msg.send()

        return dict()
