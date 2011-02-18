# -*- coding: utf-8 -*-

'''Forms and views for authentication and user information editing.'''

from __future__ import unicode_literals  # unicode by default

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid_handlers import action
from turbomail import Message
from mootiro_form import _
from mootiro_form.models import User, Form, FormCategory, SlugIdentification,\
     EmailValidationKey, sas
from mootiro_form.views import BaseView, translator, d
from mootiro_form.schemas.user import CreateUserSchema, EditUserSchema,\
     UserLoginSchema, RecoverPasswordSchema, ResendEmailValidationSchema,\
     ValidationKeySchema
from mootiro_form.utils import create_locale_cookie

def maybe_remove_password(node, remove_password=False):
    if remove_password:
        del node['password']

create_user_schema = CreateUserSchema()
edit_user_schema = EditUserSchema(after_bind=maybe_remove_password)
user_login_schema = UserLoginSchema()
recover_password_schema = RecoverPasswordSchema()
resend_email_validation_schema = ResendEmailValidationSchema()
validation_key_schema = ValidationKeySchema()


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

def resend_email_validation_form(button=_('send'), action=""):
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))
    return d.Form(resend_email_validation_schema, buttons=(button,),
                  action=action, formid='resendemailvalidationform')

def validation_key_form(button=_('send'), action=""):
    button = d.Button(title=button.capitalize(),
                      name=filter(unicode.isalpha, button))
    return d.Form(validation_key_schema, buttons=(button,), action=action,
                  formid='validationkeyform')


class UserView(BaseView):
    CREATE_TITLE = _('New user')
    EDIT_TITLE = _('Edit profile')
    LOGIN_TITLE = _('Log in')
    PASSWORD_TITLE = _('Recover password')
    VALIDATION_TITLE = _('Email validation')
    DELETE_TITLE = _('Delete profile')

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
        evk = EmailValidationKey(u)
        sas.add(u)
        sas.add(evk)
        sas.flush()

        # Sends the email verification using TurboMail
        self._send_email_validation(u, evk)

        self.request.override_renderer = 'email_validation.genshi' # Ugly!!!
        adict = dict(email_sent=True)
        return adict

    def _send_email_validation (self, user, evk):
        sender = 'donotreply@domain.org'
        recipient = user.email
        subject = _("Mootiro Form - Email Validation")
        link = self.url('email_validator', key=evk.key)

        message = _("To activate your account visit this link: ") + link
        message += _(" or use this code: ") + evk.key + _(" on ") + self.url('email_validation')

        msg = Message(sender, recipient, translator(subject))
        msg.plain = translator(message)
        msg.send()

    def _authenticate(self, user_id, ref=None, headers=[]):
        '''Stores the user_id in a cookie, for subsequent requests.'''
        if not ref:
            ref = 'http://' + self.request.registry.settings['url_root']
        headers += remember(self.request, user_id)
        # May also set max_age above. (pyramid.authentication, line 272)
        # Alternate implementation:
        # headers = remember(self.request, Authenticated)
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
        '''controls = self.request.POST.items()
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
        sas.flush()'''

        user = self.request.user
        locale = self.request.POST['language']
        user.default_locale = locale 
        settings = self.request.registry.settings
        headers = create_locale_cookie(locale, settings)

        return self._authenticate(user.id, headers=headers)

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

    @action(name='login', renderer='email_validation.genshi', request_method='POST')
    def login(self):
        adict = self.request.POST
        email   = adict['login_email']
        password = adict['login_pass']
        referrer = self.request.GET.get('ref', 'http://' + \
            self.request.registry.settings['url_root'])
        u = User.get_by_credentials(email, password)
        if u:
            if u.is_email_validated:
                 # set language cookie
                 locale = u.default_locale
                 settings = self.request.registry.settings
                 headers = create_locale_cookie(locale, settings)
                 return self._authenticate(u.id, ref=referrer, headers=headers)
            else:
                return self.email_validation_forms()
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
        '''Display the form to recover your password'''
        return dict(pagetitle=self.PASSWORD_TITLE,
                    email_form=recover_password_form().render())

    @action(name='recover', renderer='recover_password.genshi',
            request_method='POST')
    def send_recover_mail(self):
        '''Creates a slug to identify the user and sends a mail to the given
        address to enable resetting the password'''
        controls = self.request.POST.items()
        try:
            appstruct = recover_password_form().validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.PASSWORD_TITLE, email_form=e.render())
        '''Form validation passes, so create a slug and the url and send an
        email to the user to enable him to reset his password'''
        email = appstruct['email']
        user = sas.query(User).filter(User.email == email).first()
        # Create the slug to identify the user and save it in the db
        si = SlugIdentification.create_unique_slug(user)
        sas.add(si)
        sas.flush()

        # Create the url and send it to the user
        slug = si.user_slug
        password_link = self.url('user', action='reset_password') +'/'+ slug

        sender = 'donotreply@domain.org'
        recipient = email
        subject = _("Mootiro Form - Reset Password")
        message = _("To reset your password please click on the link: ")

        msg = Message(sender, recipient, translator(subject))
        msg.plain = translator(message) + password_link
        msg.send()
        return dict(pagetitle=self.PASSWORD_TITLE, email_form=None)

    @action()
    def reset_password(self):
        # fetch user via slug
        slug = self.request.matchdict['slug']
        si = sas.query(SlugIdentification) \
            .filter(SlugIdentification.user_slug == slug).one()
        # Authenticate and redirect to user_edit form
        return self._authenticate(si.user.id,
                ref=self.url('user', action='current'))

    @action(name='delete', renderer='user_delete.genshi',
            request_method='POST')
    def delete_user(self):
        ''' This view deletes the user and all data associated with her. 
        Plus, it weeps a tear for the loss of the user
        '''
        user = self.request.user
        # First of all, I delete all the data associated with the user
        for form in sas.query(Form).filter(Form.user==user):
            sas.delete(form)

        for category in sas.query(FormCategory).filter(FormCategory.user==user):
            sas.delete(category)

        # And then I delete the user. Farewell, user!
        sas.delete(user)
        sas.flush()
        
        return dict()

    @action(name='email_validator', renderer='email_validation.genshi', request_method='GET')
    def evk_validator(self):
        key = self.request.matchdict['key']
        evk = sas.query(EmailValidationKey).filter(EmailValidationKey.key == key).first()
        
        adict = dict(key=key)
        if evk:
            user = evk.user
            user.is_email_validated = True
            sas.delete(evk)
            adict["validated"] = True
        else:
            adict["invalid_key"] = True

        return adict

    @action(name='email_validation', renderer='email_validation.genshi', request_method='GET')
    def email_validation_forms(self):
        '''Display the forms to resend email validation key and the one to input
         the key code'''
        return dict(pagetitle=self.VALIDATION_TITLE, validation_needed=True,
                    email_form=resend_email_validation_form(action=self.url('email_validation')).render(),
                    key_form=validation_key_form(action=self.url('email_validation')).render())

    @action(renderer='email_validation.genshi', request_method='POST')
    def email_validation(self):
        post = self.request.POST
        email = post.get('email')
        key = post.get('key')

        # The same controls dict can validate both forms
        controls = post.items()
        
        rdict = dict()
        if email:
            try:
                appstruct = resend_email_validation_form( \
                    action=self.url('email_validation')).validate(controls)
            except d.ValidationFailure as e:
                return dict(pagetitle=self.VALIDATION_TITLE, validation_needed=True,
                            email_form=e.render(),
                            key_form=validation_key_form(action=self.url('email_validation')).render())

            user = sas.query(User).filter(User.email == email).first()
            evk = sas.query(EmailValidationKey).filter(EmailValidationKey.user == user).first()
            self._send_email_validation(user, evk)
            rdict['email_sent'] = True

        elif key:
            try:
                appstruct = validation_key_form( \
                    action=self.url('email_validation')).validate(controls)
            except d.ValidationFailure as e:
                return dict(pagetitle=self.VALIDATION_TITLE, validation_needed=True,
                            email_form=resend_email_validation_form(action=self.url('email_validation')).render(),
                            key_form=e.render())
                            
            evk = sas.query(EmailValidationKey).filter( \
                        EmailValidationKey.key == key).first()
            user = evk.user
            user.is_email_validated = True
            sas.delete(evk)
            rdict["validated"] = True

        else:
            pass

        return rdict
