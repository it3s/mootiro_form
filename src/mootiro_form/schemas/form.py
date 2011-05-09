# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d
from datetime import datetime
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
        description=_("A description for this form."))
    submit_label = c.SchemaNode(c.Str(), title=_('Submit button text'),
        default = _('Submit'), missing = _('Submit'),
        description=_("The text used in the submit button"))


class FormTestSchema(c.MappingSchema):
    nfields_ti = c.SchemaNode(c.Int(), title=_('Number of text field inputs'))
    nfields_ta = c.SchemaNode(c.Int(), title=_('Number of text area inputs'))


form_schema = FormSchema()
form_name_schema = form_schema.children[0]
# import pdb; pdb.set_trace()


def create_form_schema(form):
    '''Returns the schema of the provided `form` for entry creation purposes.
    '''
    form_schema = c.SchemaNode(c.Mapping())
    for f in form.fields:
        form_schema.add(fields_dict[f.typ.name](f).get_schema_node())
    return form_schema


# Validators
# ==========


def date_string(node, value):
    '''Checks whether the date is of the correct format to transform it into a
    datetime object'''
    if value:
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
        except:
            raise c.Invalid(node, _('Please enter a valid date of the format'
                                    ' yyyy-mm-dd hh:mm'))


def in_the_future(node, value):
    '''Checks whether the date is in the future'''
    if value:
        try:
            date = datetime.strptime(value, "%Y-%m-%d %H:%M")
        except:
            return
        if date and date < datetime.utcnow():
            raise c.Invalid(node, _('The date must be in the future'))


def valid_interval(node, value):
    if value['start_date']:
        start_date = datetime.strptime(value['start_date'], "%Y-%m-%d %H:%M")
        if value['end_date']:
            end_date = datetime.strptime(value['end_date'], "%Y-%m-%d %H:%M")
            if start_date > end_date:
                raise c.Invalid(node, _('The start date must be before'
                                        ' the end date'))


def create_public_link_restrictions_schema():
    '''A schema for the publish form tab of the form editor'''
    schema = c.SchemaNode(c.Mapping())

    interval = c.SchemaNode(c.Mapping(), name='interval',
                            validator=valid_interval)
    start_date = c.SchemaNode(c.Str(), name='start_date',
                              missing='', validator=date_string)
    end_date = c.SchemaNode(c.Str(), name='end_date',
                            missing='', validator=c.All(date_string,
                                                        in_the_future))
    interval.add(start_date)
    interval.add(end_date)
    schema.add(start_date)
    schema.add(end_date)
    schema.add(interval)

    return schema


public_link_restrictions_schema = create_public_link_restrictions_schema()

