# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from deform.widget import TextAreaWidget
from mootiro_form import _


# Minimum and maximum lengths
# ==========================

LEN_NAME = dict(min=1,)
LEN_SUBJECT = dict(min=1,)
LEN_MESSAGE = dict(min=1,)


# Schemas
# =======
class ContactFormSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Name'),
            validator=c.Length(**LEN_NAME))
    email = c.SchemaNode(c.Str(), title=_('E-mail'), validator=c.Email())
    subject = c.SchemaNode(c.Str(), title=_('Subject'),
            validator=c.Length(**LEN_SUBJECT))
    message = c.SchemaNode(c.Str(), title=_('Message'),
            widget=TextAreaWidget(cols=40, rows=12),
            validator=c.Length(**LEN_MESSAGE))
