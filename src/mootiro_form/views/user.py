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
from mootiro_form.views import BaseView, authenticated, d, get_button
from mootiro_form.schemas.user import CreateUserSchema, EditUserSchema,\
     SendMailSchema, PasswordSchema, UserLoginSchema, ValidationKeySchema
from mootiro_form.utils import create_locale_cookie
from mootiro_form.utils.form import make_form

#import logging
#logging.basicConfig()

def maybe_remove_password(node, remove_password=False):
    if remove_password:
        del node['password']

create_user_schema = CreateUserSchema()
edit_user_schema = EditUserSchema()
user_login_schema = UserLoginSchema()
send_mail_schema = SendMailSchema()
password_schema = PasswordSchema()
validation_key_schema = ValidationKeySchema()


def edit_user_form(button=_('submit'), update_password=True):
    '''Apparently, Deform forms must be instantiated for every request.'''
    return make_form(edit_user_schema, f_template='edit_profile',
                     buttons=(get_button(button),),
                     formid='edituserform')

def create_user_form(button=_('submit'), action=""):
    '''Apparently, Deform forms must be instantiated for every request.'''
    return d.Form(create_user_schema, buttons=(get_button(button),),
                  action=action, formid='createuserform')

def send_mail_form(button=_('send'), action=""):
    return d.Form(send_mail_schema, buttons=(get_button(button),),
                  action=action, formid='sendmailform')

def password_form(button=_('change password'), action=""):
    return d.Form(password_schema, buttons=(get_button(button),),
                  action=action, formid='passwordform')

def validation_key_form(button=_('send'), action=""):
    return d.Form(validation_key_schema, buttons=(get_button(button),),
                  action=action, formid='validationkeyform')

def user_login_form(button=_('log in'), action="", referrer=""):
    return d.Form(user_login_schema, action=action,
                    buttons=(get_button(button),), formid='userform')


class UserView(BaseView):
    CREATE_TITLE = _('New user')
    EDIT_TITLE = _('Edit account')
    LOGIN_TITLE = _('Log in')
    PASSWORD_TITLE = _('Change password')
    PASSWORD_SET_TITLE = _('New password set')
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
        '''Creates a new User from POSTed data and sets the locale cookie
        coherent to the language the user selected if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.params.items()
        try:
            appstruct = create_user_form(_('sign up'),
                action=self.url('user', action='new')).validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.tr(self.CREATE_TITLE), user_form = e.render())
        # Form validation passes, so create a User in the database.
        u = User(**appstruct)
        sas.add(u)
        sas.flush()

        # Set locale_cookie to the language the user selected and redirect to
        # the 'message' action (below). This is necessary to make the locale
        # cookie work for the next page and the validation email
        headers = self._set_locale_cookie()

        return HTTPFound(location=self.url('email_validation', action='message',
                         _query=dict(user_id=u.id)), headers=headers)

    @action(name='message', renderer='email_validation.genshi')
    def email_validation_message(self):
        '''sends the validation mail to the user '''
        # Fetches the user from the db via the url parameter passed in from the
        # action above
        user_id = self.request.params['user_id']
        user = sas.query(User).filter(User.id == user_id).one()
        # creates the evk and adds it to the db
        evk = EmailValidationKey(user)
        sas.add(evk)
        # Sends the email verification using TurboMail
        self._send_email_validation(user, evk)
        return dict(email_sent=True)

    def _send_email_validation(self, user, evk):
        sender = 'donotreply@domain.org'
        recipient = user.email
        subject = _("Mootiro Form - Email Validation")
        link = self.url('email_validator', action="validator", key=evk.key)

        message = self.tr(_("To activate your account visit this link:\n" \
                "{0}\n\n Or use this code:\n{1}\non {2}")) \
                .format(link, evk.key, self.url('email_validation', action="validate_key"))
        msg = Message(sender, recipient, self.tr(subject))
        msg.plain = message
        msg.send()

    def _set_locale_cookie(self):
        '''Set locale directly for the request and the locale_cookie'''
        locale = self.request.POST['default_locale']
        settings = self.request.registry.settings
        return create_locale_cookie(locale, settings)

    def _authenticate(self, user_id, ref=None, headers=[]):
        '''Stores the user_id in a cookie, for subsequent requests.'''
        if not ref:
            ref = 'http://' + self.request.registry.settings['url_root']
        headers += remember(self.request, user_id)
        # May also set max_age above. (pyramid.authentication, line 272)
        # Alternate implementation:
        return HTTPFound(location=ref, headers=headers)

    @action(name='current', renderer='user_edit.genshi', request_method='GET')
    @authenticated
    def edit_user_form(self):
        '''Displays the form to edit the current user profile.'''
        user = self.request.user
        change_password_link = self.url('user', action='edit_password')
        return dict(pagetitle=self.tr(self.EDIT_TITLE),
                    link=change_password_link, user_form=edit_user_form() \
                    .render(self.model_to_dict(user, ('nickname', 'real_name', \
                    'email', 'default_locale'))))

    @action(name='current', renderer='user_edit.genshi', request_method='POST')
    @authenticated
    def update_user(self):
        '''Saves the user profile from POSTed data if it validates;
        else redisplays the form with the error messages.
        '''
        controls = self.request.POST.items()
        uf = edit_user_form()
        # Validate the instantiated form against the controls
        try:
            appstruct = uf.validate(controls)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(pagetitle=self.tr(self.EDIT_TITLE), user_form = e.render())
        # Form validation passes, so save the User in the database.
        user = self.request.user
        self.dict_to_model(appstruct, user) # update user
        sas.flush()
        # And set the language cookie, so the user browses directly with the
        # selected language
        headers = self._set_locale_cookie()

        return self._authenticate(user.id, headers=headers)

    @action(name='edit_password', renderer='edit_password.genshi',
            request_method ='GET')
    @authenticated
    def show_password_form(self):
        '''Displays the form to edit the user's password.'''
        return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                    password_form=password_form().render())

    @action(name='edit_password', renderer='edit_password.genshi',
            request_method = 'POST')
    @authenticated
    def update_password(self):
        '''Updates the user's password and redirects back to the edit profile
        view.
        '''
        # validate instatiated form against the controls
        controls = self.request.POST.items()
        try:
            appstruct = password_form().validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                        password_form=e.render())
        # Form validation passes, so update the password in the database.
        user = self.request.user
        self.dict_to_model(appstruct, user) # save password
        sas.flush()
        link = self.url('user', action='current')
        return dict(changed=True, link=link, pagetitle=self.tr(self.PASSWORD_TITLE),
                    password_form=None)

    @action(name='login', renderer='user_login.genshi', request_method='GET')
    def login_form(self):
        referrer = self.request.GET.get('ref', 'http://' + \
            self.request.registry.settings['url_root'])

        form = user_login_form(action=self.url('user', action='login', _query=[('ref', referrer)]),
                referrer=referrer).render()
        return dict(pagetitle=self.tr(self.LOGIN_TITLE), user_login_form=form, referrer=referrer)

    @action(name='login', renderer='email_validation.genshi', request_method='POST')
    def login(self):
        adict = self.request.POST
        email = adict['login_email']
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
                return self.validate_key_form()
        else:
            referrer = referrer + "?login_error=True"
            return HTTPFound(location=referrer)

    @action(request_method='POST')
    def logout(self):
        '''Creates HTTP headers that cause the authentication cookie to be
        deleted and redirects to the front page.
        '''
        headers = forget(self.request)
        return HTTPFound(location='http://' + \
            self.request.registry.settings['url_root'], headers=headers)

    @action(name='send_recover_mail', renderer='recover_password.genshi',
            request_method='GET')
    def forgotten_password(self):
        '''Display the form to send an email to the user to enable him to
        change his password.
        '''
        return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                    email_form=send_mail_form().render())

    @action(name='send_recover_mail', renderer='recover_password.genshi',
            request_method='POST')
    def send_recover_mail(self):
        '''Creates a slug to identify the user and sends a mail to the given
        address to enable resetting the password.
        '''
        controls = self.request.POST.items()
        try:
            appstruct = send_mail_form().validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                email_form=e.render())
        '''Form validation passes, so create a slug and the url and send an
        email to the user to enable him to reset his password.'''
        email = appstruct['email']
        user = sas.query(User).filter(User.email == email).first()
        # Create the slug to identify the user and save it in the db
        si = SlugIdentification.create_unique_slug(user)
        sas.add(si)
        sas.flush()

        # Create the url and send it to the user
        slug = si.user_slug
        password_link = self.url('reset_password', action='recover', slug=slug)

        sender = 'donotreply@domain.org'
        recipient = email
        subject = _("Mootiro Form - Change Password")
        message = _("To change your password please click on the link: ")

        msg = Message(sender, recipient, self.tr(subject))
        msg.plain = self.tr(message) + password_link
        msg.send()
        return dict(pagetitle=self.tr(self.PASSWORD_TITLE), email_form=None)

    @action(name='recover', renderer='enter_new_password.genshi',
            request_method='GET')
    def receive_password(self):
        slug = self.request.matchdict['slug']
        si = sas.query(SlugIdentification) \
                .filter(SlugIdentification.user_slug == slug).first()
        if si:
            # render form if password was not yet resetted
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                        password_form=password_form().render(), invalid=False, \
                        resetted=False)
        else:
            # render 'Password was already resetted'
            url = self.url('user', action='send_recover_mail')
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                        password_form=None, invalid=True, \
                        resetted=False, link=url)

    @action(name='recover', renderer='enter_new_password.genshi',
            request_method='POST')
    def alter_password(self):
        # fetch user via slug
        slug = self.request.matchdict['slug']
        try:
            si = sas.query(SlugIdentification) \
                .filter(SlugIdentification.user_slug == slug).one()
        except:
            url = self.url('user', action='send_recover_mail')
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE), password_form=None,
                        invalid=True, resetted=False, link=url)
        user = si.user
        # and delete the slug afterwards so the email link can only be used once
        sas.delete(si)
        # validate instatiated form against the controls
        controls = self.request.POST.items()
        try:
            appstruct = password_form().validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.tr(self.PASSWORD_TITLE),
                        password_form=e.render(),
                        invalid=False, resetted=False)
        # save new password in the database
        new_password = appstruct['password']
        user.password = new_password
        return dict(pagetitle=self.tr(self.PASSWORD_SET_TITLE), password_form=None,
                    resetted=True, invalid=False)

    @action(name='delete', renderer='user_delete.genshi',
            request_method='POST')
    def delete_user(self):
        ''' This view deletes the user and all data associated with her.
        Plus, it weeps a tear for the loss of the user.
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

    @action(name='validator', renderer='email_validation.genshi')
    def validator(self):
        key = self.request.matchdict['key']
        evk = sas.query(EmailValidationKey) \
                .filter(EmailValidationKey.key == key).first()

        rdict = dict(key=key)
        if not evk:
            rdict["invalid_key"] = True
        else:
            self._validate(evk)
            rdict["validated"] = True

        return rdict

    def _validate(self, evk):
        if not evk: return False

        user = evk.user
        user.is_email_validated = True
        sas.delete(evk)
        return True

    @action(name='validate_key', renderer='email_validation.genshi', request_method='GET')
    def validate_key_form(self):
        '''Display the form to input the key code.'''
        return dict(pagetitle=self.tr(self.VALIDATION_TITLE),
                    key_form=validation_key_form(action=self
                        .url('email_validation', action="validate_key")).render())

    @action(name='validate_key', renderer='email_validation.genshi', request_method='POST')
    def validate_key(self):
        post = self.request.POST
        key = post.get('key')

        rdict = dict()

        controls = post.items()
        try:
            validation_key_form( \
                action=self.url('email_validation', action="validate_key")) \
                        .validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.tr(self.VALIDATION_TITLE),
                    key_form=e.render())

        evk = sas.query(EmailValidationKey).filter( \
                    EmailValidationKey.key == key).first()
        self._validate(evk)
        rdict["validated"] = True

        return rdict

    @action(name='resend', renderer='email_validation.genshi', request_method='GET')
    def resend_email_form(self):
        '''Display the forms to resend email validation key.'''
        return dict(pagetitle=self.tr(self.VALIDATION_TITLE),
                    email_form=send_mail_form(action=self
                        .url('email_validation', action="resend")).render())

    @action(name='resend', renderer='email_validation.genshi', request_method='POST')
    def resend_email(self):
        post = self.request.POST
        email = post.get('email')

        rdict = dict()
        
        controls = post.items()
        try:
            send_mail_form( \
                action=self.url('email_validation', action="resend")) \
                    .validate(controls)
        except d.ValidationFailure as e:
            return dict(pagetitle=self.tr(self.VALIDATION_TITLE),
                        email_form=e.render())

        user = sas.query(User).filter(User.email == email).first()
        evk = sas.query(EmailValidationKey) \
            .filter(EmailValidationKey.user == user).first()

        if not evk:
            rdict['invalid_email'] = True
            rdict.update(**self.resend_email_form())
        else:
            self._send_email_validation(user, evk)
            rdict['email_sent'] = True

        return rdict
