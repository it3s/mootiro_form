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
        missing='',
        validator=c.Length(min=0, max=length(Form.name)))
    description = c.SchemaNode(c.Str(), title=_('Description'),
        widget = d.widget.TextAreaWidget(rows=5),
        default = '', missing = '',
        description=_("A long description for this form."))
    submit_label = c.SchemaNode(c.Str(), title=_('Submit Label'),
        default = _('Submit'), missing = _('Submit'),
        description=_("The text used in the submit button"))


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
    for f in entry.form.fields:
        form_schema.add(fields_dict[f.typ.name](f).get_schema_node())
    return form_schema
