# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

# import deform as d
import colander as c
from mootiro_form import _
from mootiro_form.models import Form, length


class FormSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Form title'),
        description=_("A name for this form."),
        validator=c.Length(min=2, max=length(Form.name)))


class FormTestSchema(c.MappingSchema):
    nfields_ti = c.SchemaNode(c.Int(), title=_('Number of text field inputs'))
    nfields_ta = c.SchemaNode(c.Int(), title=_('Number of text area inputs'))

form_schema = FormSchema()
