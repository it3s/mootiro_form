# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
from pyramid_handlers import action

from mootiro_form import _
from mootiro_form.models import User, sas
from mootiro_form.views import BaseView, d

import colander as c

class UserLoginSchema(c.MappingSchema):
    login_email = c.SchemaNode(c.Str(), title=_('E-mail'),
                         validator=c.Email())
    login_pass = c.SchemaNode(c.Str(), title=_('Password'),
        validator=c.Length(min=8, max=40),
        widget = d.widget.PasswordWidget())

def unique_email(node, value):
    if sas.query(User).filter(User.email == value).one():
        raise c.Invalid(node, _('An account with this email already exist in the system.'))

def unique_nickname(node, value):
    if sas.query(User).filter(User.nickname == value).one():
        raise c.Invalid(node, _('An account with this nickname already exist in the system.'))

class UserSchema(c.MappingSchema):
    nickname  = c.SchemaNode(c.Str(), title=_('Nickname'),
        description=_("a short name for you, without spaces"), size=20,
        validator=c.All(c.Length(min=1, max=32), unique_nickname))
    real_name = c.SchemaNode(c.Str(), title=_('Real name'),
        validator=c.Length(min=5, max=240))
    email     = c.SchemaNode(c.Str(), title=_('E-mail'),
                                validator=c.All(c.Email(), unique_email))
    password  = c.SchemaNode(c.Str(), title=_('Password'),
        validator=c.Length(min=8, max=40),
        widget = d.widget.CheckedPasswordWidget())
    # TODO: Verify i18n.   http://deformdemo.repoze.org/i18n/
    # TODO: Fix password widget appearance (in CSS?)
    # TODO: Add a "good password" validator or something. Here are some ideas:
        # must be 6-20 characters in length
        # must have at least one number and one letter
        # must be different from the username and email
        # can contain spaces?
        # is case-sensitive.
    # TODO: Get `max` values from the model, after upgrading to SQLAlchemy 0.7

def maybe_remove_password(node, remove=False):
    if remove:
        del node['password']

user_schema = UserSchema(after_bind=maybe_remove_password)
user_login_schema = UserLoginSchema()

def user_form(button=_('submit'), update_password=True):
    '''Apparently, Deform forms must be instantiated for every request.'''
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))

    if not update_password:
        us = user_schema.bind(remove=True)
    else:
        us = user_schema

    return d.Form(us, buttons=(button,), formid='userform')

class UserView(BaseView):
    CREATE_TITLE = _('New user')
    EDIT_TITLE = _('Edit profile')
    LOGIN_TITLE = _('Log in')

    @action(name='new', renderer='user_edit.genshi', request_method='GET')
    def new_user_form(self):
        '''Displays the form to create a new user.'''
        return dict(pagetitle=self.tr(self.CREATE_TITLE),
            user_form=user_form(_('sign up')).render())

    @action(name='new', renderer='user_edit.genshi', request_method='POST')
    def save_new_user(self):
        '''Creates a new User from POSTed data if it validates;
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
        return self._authenticate(u.id)

    def _authenticate(self, user_id, ref="/"):
        '''Stores the user_id in a cookie, for subsequent requests.'''
        headers = remember(self.request, user_id) # really say user_id here?
        # May also set max_age above. (pyramid.authentication, line 272)

        # Alternate implementation:
        # headers = remember(self.request, Authenticated)
        # May also set max_age above. (pyramid.authentication, line 272)

        # Another way would be to implement session-based auth/auth.
        # session['user_id'] = user_id
        return HTTPFound(location=ref, headers=headers)

    @action(name='current', renderer='user_edit.genshi', request_method='GET')
    def edit_user_form(self):
        '''Displays the form to edit the current user profile.'''
        user = self.request.user
        return dict(pagetitle=self.EDIT_TITLE,
            user_form=user_form().render(self.model_to_dict(user,
                ('nickname', 'real_name', 'email', 'password'))))

    @action(name='current', renderer='user_edit.genshi', request_method='POST')
    def update_user(self):
        '''Saves the user profile from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.POST.items()
        # If password not provided, instantiate a user form without password
        if not self.request.POST['value'] and \
           not self.request.POST['confirm']:
            uf = user_form(update_password=False)
        else:
            uf = user_form()
        # Validate the instantiated form against the controls
        try:
            appstruct = uf.validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.EDIT_TITLE, user_form = e.render())
        # Form validation passes, so save the User in the database.
        user = self.request.user
        self.dict_to_model(appstruct, user) # update user
        sas.flush()
        return self._authenticate(user.id)

    @action(name='login', renderer='user_login.genshi', request_method='GET')
    def login_form(self):
        referrer = self.request.GET.get('ref', '/')
        button = d.Button(title=_('Log in'), name=_('Log in'))
        user_login_form = d.Form(user_login_schema,
                action=self.url('user', action='login',
                                _query=[('ref', referrer)]),
                buttons=(button,), formid='userform')
        return dict(pagetitle=self.tr(self.LOGIN_TITLE),
            user_login_form=user_login_form.render())

    @action(name='login', request_method='POST')
    def login(self):
        adict = self.request.POST
        email   = adict['login_email']
        password = adict['login_pass']
        referrer = self.request.GET.get('ref', '/')
        u = User.get_by_credentials(email, password)
        if u:
            return self._authenticate(u.id, ref=referrer)
        else:
            # TODO: Redisplay the form, maybe with a...
            # self.request.session.flash(
            #    'Sorry, wrong credentials. Please try again.')
            return HTTPFound(location=referrer)

    @action(request_method='POST')
    def logout(self):
        '''Creates HTTP headers that cause the authentication cookie to be
        deleted and redirects to the front page.
        '''
        headers = forget(self.request)
        return HTTPFound(location='/', headers=headers)

    @action()
    def forgotten_password(self):
        # TODO: Implement
        return Response('forgotten_password()')


# TODO: Send e-mail and demand confirmation from the user

# TODO: Add a way to delete a user. Careful: this has enormous implications
# for the database.
