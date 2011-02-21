# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d
from mootiro_form import _
from mootiro_form.models import Form, length
from mootiro_form.fieldtypes import fields_dict

class FormSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Form title'), # TODO: maxlength=255,
        description=_("A name for this form."),
        validator=c.Length(min=2, max=length(Form.name)))


class FormTestSchema(c.MappingSchema):
    nfields_ti = c.SchemaNode(c.Int(), title=_('Number of text field inputs'))
    nfields_ta = c.SchemaNode(c.Int(), title=_('Number of text area inputs'))

form_schema = FormSchema()

def create_form_schema(form):
    form_schema = c.SchemaNode(c.Mapping())
    for f in form.fields:
        form_schema.add(fields_dict[f.typ.name](f).get_schema_node())
    return form_schema

def create_form_entry_schema(entry):
    form_schema = c.SchemaNode(c.Mapping())
    field_data_dict = dict([(e.field_id, e.value) for e in entry.textinput_data])
    for f in entry.form.fields:
        form_schema.add(fields_dict[f.typ.name](f).get_schema_node())
    return form_schema
