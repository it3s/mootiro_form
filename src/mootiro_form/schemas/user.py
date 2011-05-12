# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import deform as d
import colander as c
from mootiro_form import _, enabled_locales
from mootiro_form.models import sas, User, length, EmailValidationKey


# Validators
# ==========

def unique_email(node, value):
    if sas.query(User).filter(User.email == value).first():  # may return None
        raise c.Invalid(node, _('An account with this email already exists.'))


def email_exists(node, value):
    if not sas.query(User).filter(User.email == value).first():
        raise c.Invalid(node, _('There is no account with this email.'))


def unique_nickname(node, value):
    if sas.query(User).filter(User.nickname == value).first():
        raise c.Invalid(node,
            _('An account with this nickname already exists.'))

def key_exists(node, value):
    if not sas.query(EmailValidationKey).filter(EmailValidationKey.key == value) \
            .first():
        raise c.Invalid(node, _('The given key is invalid.'))

def locale_exists(node, value):
    locales = []
    for adict in enabled_locales:
        locales.append(adict['name'])
    if not value in locales:
        raise c.Invalid(node, _('Please select a language'))

def is_checked(node, value):
    if value == False:
        raise c.Invalid(node, _('You have to agree to the terms of service'))

# Minimum and maximum lengths
# ===========================

LEN_REAL_NAME = dict(min=5, max=length(User.real_name))
LEN_PASSWORD = dict(min=8, max=User.LEN_PASSWORD)
LEN_NICKNAME = dict(min=1, max=length(User.nickname))


# Fields used more than once
# ==========================


def real_name():
    return c.SchemaNode(c.Str(), title=_('Real name'),
            description=_('Minimum length 5 characters'),
            validator=c.Length(**LEN_REAL_NAME),
            widget=d.widget.TextInputWidget(template='textinput_descr'))


def email_existent():
    return c.SchemaNode(c.Str(), title=_('E-mail'),
                        validator=c.All(c.Email(), email_exists))


def email_is_unique():
    return c.SchemaNode(c.Str(), title=_('E-mail'),
                        validator=c.All(c.Email(), unique_email),
                        description=_("Enter a valid email address"),
                        widget=d.widget.TextInputWidget(template='textinput_descr'))


def password():
    return c.SchemaNode(c.Str(), title=_('Password'),
                        description=_('Minimum 8 characters. Please mix ' \
                                      'letters and numbers'),
                        validator=c.Length(**LEN_PASSWORD),
                        widget=d.widget.CheckedPasswordWidget())


def language_dropdown():
    return c.SchemaNode(c.Str(), title=_('Language'),
                        validator=locale_exists,
                        widget=d.widget.SelectWidget(values=( \
                            ('choose', _('--Choose--')), ('en', _('English')), \
                            ('pt_BR', _('Portuguese')))))


# Schemas
# =======

class CreateUserSchema(c.MappingSchema):
    nickname = c.SchemaNode(c.Str(), title=_('Nickname'),
        description=_("A short name for you, without spaces. " \
                      "This cannot be changed later!"), size=20,
        validator=c.All(c.Length(**LEN_NICKNAME), unique_nickname),
        widget=d.widget.TextInputWidget(template='textinput_descr'))
    real_name = real_name()
    email = email_is_unique()
    default_locale = language_dropdown()
    terms_of_service = c.SchemaNode(c.Bool(), validator=is_checked,
        widget=d.widget.CheckboxWidget(template='checkbox_terms'))
    password = password()

class EditUserSchema(c.MappingSchema):
    real_name = real_name()
    email = email_is_unique()
    default_locale = language_dropdown()

class EditUserSchemaWithoutMailValidation(c.MappingSchema):
    real_name = real_name()
    email = c.SchemaNode(c.Str(), title=_('E-mail'),
              validator=c.Email(),
              description=_("Enter a valid email address"),
              widget=d.widget.TextInputWidget(template='textinput_descr'))
    default_locale = language_dropdown()

class SendMailSchema(c.MappingSchema):
    email = email_existent()

class PasswordSchema(c.MappingSchema):
    password = password()

class ValidationKeySchema(c.MappingSchema):
    key = c.SchemaNode(c.Str(), title=_('Key'),
            validator=key_exists)

class UserLoginSchema(c.MappingSchema):
    login_email = c.SchemaNode(c.Str(), title=_('E-mail'),
                               validator=c.Email())
    login_pass = c.SchemaNode(c.Str(), title=_('Password'),
        validator=c.Length(**LEN_PASSWORD),
        widget=d.widget.PasswordWidget())


# TODO: Verify i18n.   http://deformdemo.repoze.org/i18n/
# TODO: Fix password widget appearance (in CSS?)
# TODO: Add a "good password" validator or something. Here are some ideas:
    # must be 6-20 characters in length
    # must have at least one number and one letter
    # must be different from the username and email
    # can contain spaces?
    # is case-sensitive.
