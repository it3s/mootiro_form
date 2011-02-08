# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid_handlers import action
from mootiro_form.models import User, sas
from mootiro_form.views import BaseView

from turbomail import Message
from turbomail.control import interface


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

        return dict(forms=user.forms)

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
        if locale in settings['enabled_locales']:
            headers = [('Set-Cookie',
                '_LOCALE_={0}; expires=31 Dec 2050 23:00:00 GMT; Path=/'.format(locale))]
        else:
            headers = None
        return HTTPFound(location=location, headers=headers)

    @action(name='contact', renderer='contact.genshi', request_method='GET')
    def show_contact_form(self):
        '''Shows the contact form'''
        return dict()
        
    @action(name='contact', renderer='contact_successful.genshi', request_method='POST')
    def sendmail(self):
        '''Handles the form for sending contact emails'''
        
        adict = self.request.POST
        
        name = adict['name']
        email = adict['email']
        subject = adict['subject']
        message = adict['message']
        
        if email == "":
            return render_to_response('contact.genshi', {"name": name,
            "subject": subject, "message": message, "missing_email": True}, request=self.request)
        
        turbomail_config = {
            'mail.on': True,
            'mail.transport': 'smtp',
            'mail.smtp.server': 'localhost',
            'mail.manager': 'immediate'
        }
        msg = Message(email, "institute@it3s.org", subject)
        msg.plain = message
        interface.start(turbomail_config)
        msg.send()
        interface.stop()

        return dict()
       
