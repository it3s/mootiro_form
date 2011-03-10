# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from deform.widget import TextAreaWidget
from mootiro_form import _


class Contact(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Name  '), validator=c.Range(min=1))
    email = c.SchemaNode(c.Str(), title=_('E-Mail '), validator=c.Email())
    subject = c.SchemaNode(c.Str(), title=_('Subject'),
            validator=c.Range(min=1))
    message = c.SchemaNode(c.Str(), title=_('Message'),
            widget=TextAreaWidget(cols=40, rows=12),
            validator=c.Range(min=1))
