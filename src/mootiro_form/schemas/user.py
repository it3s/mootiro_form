# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import deform as d
import colander as c
from mootiro_form import _, enabled_locales
from mootiro_form.models import sas, User, length, EmailValidationKey


# Validators
# ==========

def unique_email(node, value):
    # We use ilike() so the email search is case-insensitive
    if sas.query(User).filter(User.email.ilike(value)).count():
        raise c.Invalid(node, _('An account with this email already exists.'))


def email_exists(node, value):
    if not sas.query(User).filter(User.email == value).first():
        raise c.Invalid(node, _('We do not recognize this email. Perhaps you used another one when signing up.'))


def unique_nickname(node, value):
    if sas.query(User).filter(User.nickname == value).first():
        raise c.Invalid(node,
            _('This nickname already exists. Please choose a different one.'))


def key_exists(node, value):
    if not sas.query(EmailValidationKey) \
            .filter(EmailValidationKey.key == value).first():
        raise c.Invalid(node, _('Invalid key. Your email may have been validated already.'))


def locale_exists(node, value):
    locales = []
    for adict in enabled_locales:
        locales.append(adict['name'])
    if not value in locales:
        raise c.Invalid(node, _('Please select a language.'))


def is_checked(node, value):
    if value == False:
        raise c.Invalid(node, _('You have to agree to the Terms of Service.'))


# Minimum and maximum lengths
# ===========================

LEN_REAL_NAME = dict(min=5, max=length(User.real_name))
LEN_PASSWORD = dict(min=8, max=User.LEN_PASSWORD)
LEN_NICKNAME = dict(min=1, max=length(User.nickname))


# Fields used more than once
# ==========================

def real_name():
    return c.SchemaNode(c.Str(), title=_('Full name'), name='real_name',
            description=_('At least five characters.'),
            validator=c.Length(**LEN_REAL_NAME),
            widget=d.widget.TextInputWidget(template='textinput_descr'))


def email_existent():
    return c.SchemaNode(c.Str(), title=_('Email'),
                        validator=c.All(c.Email(), email_exists))


def email_is_unique():
    return c.SchemaNode(c.Str(), title=_('Email'), name='email',
                validator=c.All(c.Email(), unique_email),
                description=_("Enter a valid email address."),
                widget=d.widget.TextInputWidget(template='textinput_descr'))


def password():
    return c.SchemaNode(c.Str(), title=_('Password'), name='password',
                        description=_('Minimum 8 characters. Please mix ' \
                                      'letters and numbers'),
                        validator=c.Length(**LEN_PASSWORD),
                        widget=d.widget
                            #assign category as structural to make the
                            #description label of a field disappear.
                            .CheckedPasswordWidget(category='structural'))


def language_dropdown():
    return c.SchemaNode(c.Str(), title=_('Language'), name='default_locale',
                        validator=locale_exists,
                        widget=d.widget.SelectWidget(values=( \
                            ('choose', _('--Choose--')), ('en', _('English')), \
                            ('pt_BR', _('Portuguese')))))


# Schemas
# =======

def create_user_schema(add_terms):
    nickname = c.SchemaNode(c.Str(), title=_('Nickname'), name='nickname',
        description=_("A short name for you, without spaces. " \
                      "This cannot be changed later!"), size=20,
        validator=c.All(c.Length(**LEN_NICKNAME), unique_nickname),
        widget=d.widget.TextInputWidget(template='textinput_descr'))
    reel_name = real_name()
    email = email_is_unique()
    default_locale = language_dropdown()
    terms_of_service = c.SchemaNode(c.Bool(), title=_('Terms of Service'),
        validator=is_checked, name='terms_of_service',
        widget=d.widget.CheckboxWidget(template='checkbox_terms'))
    passw = password()
    user_schema=c.SchemaNode(c.Mapping(), nickname, reel_name, email,
            default_locale, passw)
    if add_terms == 'true':
        user_schema.add(terms_of_service)
    return user_schema


class EditUserSchema(c.MappingSchema):
    real_name = real_name()
    email = email_is_unique()
    default_locale = language_dropdown()


class EditUserSchemaWithoutMailValidation(c.MappingSchema):
    real_name = real_name()
    email = c.SchemaNode(c.Str(), title=_('Email'),
              validator=c.Email(),
              description=_("Enter a valid email address."),
              widget=d.widget.TextInputWidget(template='textinput_descr'))
    default_locale = language_dropdown()


class SendMailSchema(c.MappingSchema):
    email = email_existent()


class PasswordSchema(c.MappingSchema):
    password = password()


class ValidationKeySchema(c.MappingSchema):
    key = c.SchemaNode(c.Str(), title=_('Validation key'),
            validator=key_exists)


class UserLoginSchema(c.MappingSchema):
    login_email = c.SchemaNode(c.Str(), title=_('Email'),
                               validator=c.Email())
    login_pass = c.SchemaNode(c.Str(), title=_('Password'),
        validator=c.Length(**LEN_PASSWORD),
        widget=d.widget.PasswordWidget())


# TODO: Fix password widget appearance (in CSS?)
# TODO: Add a "good password" validator or something. Here are some ideas:
    # must be 6-20 characters in length
    # must have at least one number and one letter
    # must be different from the username and email
    # can contain spaces?
    # is case-sensitive.
