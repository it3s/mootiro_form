# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid_handlers import action

from mootiro_form import _
from mootiro_form.models import User, sas
from mootiro_form.views import BaseView, d
from mootiro_form.schemas.user import CreateUserSchema, EditUserSchema,\
    UserLoginSchema, RecoverPasswordSchema

def maybe_remove_password(node, remove_password=False):
    if remove_password:
        del node['password']

create_user_schema = CreateUserSchema()
edit_user_schema = EditUserSchema(after_bind=maybe_remove_password)
user_login_schema = UserLoginSchema()
recover_password_schema = RecoverPasswordSchema()

def edit_user_form(button=_('submit'), update_password=True):
    '''Apparently, Deform forms must be instantiated for every request.'''
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))

    if not update_password:
        eus = edit_user_schema.bind(remove_password=True)
    else:
        eus = edit_user_schema

    return d.Form(eus, buttons=(button,), formid='edituserform')

def create_user_form(button=_('submit'), action=""):
    '''Apparently, Deform forms must be instantiated for every request.'''
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))

    return d.Form(create_user_schema, buttons=(button,), action=action,
        formid='createuserform')

def recover_password_form(button=_('send'), action=""):
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))

    return d.Form(recover_password_schema, buttons=(button,), action=action,
                  formid='recoverpasswordform')


class UserView(BaseView):
    CREATE_TITLE = _('New user')
    EDIT_TITLE = _('Edit profile')
    LOGIN_TITLE = _('Log in')
    PASSWORD_TITLE = _('Recover password')

    @action(name='new', renderer='user_edit.genshi', request_method='GET')
    def new_user_form(self):
        '''Displays the form to create a new user.'''
        return dict(pagetitle=self.tr(self.CREATE_TITLE),
            user_form=create_user_form(_('sign up'),
            action=self.url('user', action='new')).render())

    @action(name='new', renderer='user_edit.genshi', request_method='POST')
    def save_new_user(self):
        '''Creates a new User from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        try:
            appstruct = create_user_form(_('sign up'),
            action=self.url('user', action='new')).validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.CREATE_TITLE, user_form = e.render())
        # Form validation passes, so create a User in the database.
        u = User(**appstruct)
        sas.add(u)
        sas.flush()
        return self._authenticate(u.id)

    def _authenticate(self, user_id, ref=None):
        '''Stores the user_id in a cookie, for subsequent requests.'''
        if not ref:
            ref = 'http://' + self.request.registry.settings['url_root']
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
            user_form=edit_user_form().render(self.model_to_dict(user,
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
            uf = edit_user_form(update_password=False)
        else:
            uf = edit_user_form()
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
        referrer = self.request.GET.get('ref', 'http://' + \
            self.request.registry.settings['url_root'])
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
        referrer = self.request.GET.get('ref', 'http://' + \
            self.request.registry.settings['url_root'])
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
        return HTTPFound(location='http://' + \
            self.request.registry.settings['url_root'], headers=headers)

    @action(name='recover', renderer='recover_password.genshi',
            request_method='GET')
    def forgotten_password(self):
        '''Display the form to recover your password)'''
        return dict(pagetitle=self.PASSWORD_TITLE,
                    email_form=recover_password_form().render())

    @action(name='recover', renderer='recover_password.genshi',
            request_method='POST')
    def send_recover_mail(self):
        '''Creates a slug to identify the user and sends a mail to the given
        address to enable resetting the password'''
        email = self.request.params.items()
        try:
            appstruct = recover_password_form().validate(email)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.PASSWORD_TITLE, email_form=e.render())
        '''Form validation passes, so create a slug and the url and send an
        email to the user to enable him to reset his password'''

        u = User(**appstruct)
        sas.add(u)
        sas.flush()
        return self._authenticate(u.id)

# TODO: Send e-mail and demand confirmation from the user

# TODO: Add a way to delete a user. Careful: this has enormous implications
# for the database.
