from mootiro_form import _
from mootiro_form.models import sas
from mootiro_form.models.user import User
from mootiro_form.views import BaseView, d, c

class UserLoginSchema(c.MappingSchema):
    login_email = c.SchemaNode(c.Str(), title=_('E-mail'),
                         validator=c.Email())
    login_pass = c.SchemaNode(c.Str(), title=_('Password'),
        validator=c.Length(min=8, max=40),
        widget = d.widget.PasswordWidget())

def unique_email(node, value):
    if sas.query(User).filter(User.email == value).first(): # may return None
        raise c.Invalid(node, _('An account with this email already exists.'))

def unique_nickname(node, value):
    if sas.query(User).filter(User.nickname == value).first(): # may return None
        raise c.Invalid(node,
            _('An account with this nickname already exists.'))

class CreateUserSchema(c.MappingSchema):
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

class EditUserSchema(c.MappingSchema):
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
