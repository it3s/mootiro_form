# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

# import deform as d
import colander as c
from mootiro_form import _
from mootiro_form.models import Form, length


class FormSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Form title'),
        description=_("A short name for you, without spaces. " \
                      "This cannot be changed later!"), size=26,
        validator=c.Length(min=2, max=length(Form.name)))


form_schema = FormSchema()

