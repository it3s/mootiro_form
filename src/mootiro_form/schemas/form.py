# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

# import deform as d
import colander as c
import deform as d
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

def field_schema(field):
    if field.typ.name == 'TextInput':
        return c.SchemaNode(c.Str(), title=field.label,
            name='input-{0}'.format(field.id),
            description=field.description,
            **({} if field.required else {'missing': ''})
            )
    elif field.typ.name == 'TextArea':
        return c.SchemaNode(c.Str(), title=field.label,
            name='input-{0}'.format(field.id),
            description=field.description,
            widget=d.widget.TextAreaWidget(rows=5),
            **({} if field.required else {'missing': ''})
            )

def create_form_schema(form):
    form_schema = c.SchemaNode(c.Mapping())

    for field in form.fields:
        form_schema.add(field_schema(field))

    return form_schema
