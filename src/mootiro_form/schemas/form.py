# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
import colander as c
import deform as d
from mootiro_form import _
from mootiro_form.models import Form, length
from mootiro_form.fieldtypes import fields_dict


class FormSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Form title'),
        description=_("name your form"),
        missing='',
        validator=c.Length(min=0, max=length(Form.name)))
    description = c.SchemaNode(c.Str(), title=_('Description'),
        widget = d.widget.TextAreaWidget(rows=5),
        default = '', missing = '',
        description=_("description of this form"))
    submit_label = c.SchemaNode(c.Str(), title=_('Text for "Submit" button'),
        default = _('Submit'), missing = _('Submit'),
        description=_("name of the button used to submit the form"))

form_schema = FormSchema()
form_name_schema = form_schema.children[0]


def create_form_schema(form):
    '''Returns the schema of the provided `form` for entry creation purposes.
    '''
    form_schema = c.SchemaNode(c.Mapping())
    for f in form.fields:
        form_schema.add(fields_dict[f.typ.name](f).get_schema_node())
    return form_schema
