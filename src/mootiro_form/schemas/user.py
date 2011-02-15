# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import deform as d
import colander as c
from mootiro_form import _
from mootiro_form.models import sas, User, length

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


# Minimum and maximum lengths
# ===========================

LEN_REAL_NAME = dict(min=5, max=length(User.real_name))
LEN_PASSWORD = dict(min=8, max=User.LEN_PASSWORD)
LEN_NICKNAME = dict(min=1, max=length(User.nickname))


# Fields used more than once
# ==========================
real_name = c.SchemaNode(c.Str(), title=_('Real name'),
                         validator=c.Length(**LEN_REAL_NAME))
email = c.SchemaNode(c.Str(), title=_('E-mail'),
                     validator=c.All(c.Email(), unique_email))
password = c.SchemaNode(c.Str(), title=_('Password'),
                        validator=c.Length(**LEN_PASSWORD),
                        widget=d.widget.CheckedPasswordWidget())


# Schemas
# =======

class CreateUserSchema(c.MappingSchema):
    nickname = c.SchemaNode(c.Str(), title=_('Nickname'),
        description=_("A short name for you, without spaces. " \
                      "This cannot be changed later!"), size=20,
        validator=c.All(c.Length(**LEN_NICKNAME), unique_nickname))
    real_name = real_name
    email = email
    password = password


class EditUserSchema(c.MappingSchema):
    real_name = real_name
    email = email
    password = password


class RecoverPasswordSchema(c.MappingSchema):
    email = c.SchemaNode(c.Str(), title=_('E-mail'),
            validator=c.All(c.Email(), email_exists))

# TODO: factorate ResendEmailValidationSchema and RecoverPasswordSchema
class ResendEmailValidationSchema(c.MappingSchema):
    email = c.SchemaNode(c.Str(), title=_('E-mail'),
            validator=c.All(c.Email(), email_exists))

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
