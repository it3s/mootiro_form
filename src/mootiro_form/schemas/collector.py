# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c

from datetime import datetime

from mootiro_form import _
from mootiro_form.schemas import web_url  # a URL validator
from mootiro_form.models import get_length
from mootiro_form.models.collector import PublicLinkCollector, Collector


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


# Schemas
# =======

def create_public_link_schema():
    name = c.SchemaNode(c.Str(), name='name',
        validator=c.Length(max=get_length(PublicLinkCollector, 'name')))
    on_completion = c.SchemaNode(c.Str(), name='on_completion',
        validator=c.OneOf(Collector.ON_COMPLETION_VALUES))
    thanks_url = c.SchemaNode(c.Str(), name='thanks_url', missing='',
        validator=c.All(c.Length(max=get_length(Collector, 'thanks_url')),
            web_url))
    thanks_message = c.SchemaNode(c.Str(), name='thanks_message', missing='')
    limit_by_date = c.SchemaNode(c.Boolean(), name='limit_by_date',
            missing=False)
    message_after_end = c.SchemaNode(c.Str(), name='message_after_end',
            missing='')
    message_before_start = c.SchemaNode(c.Str(), name='message_before_start',
            missing='')
    start_date = c.SchemaNode(c.Str(), name='start_date',
                              missing='', validator=date_string)
    end_date = c.SchemaNode(c.Str(), name='end_date',
                            missing='', validator=c.All(date_string,
                                                        in_the_future))
    public_link_schema = c.SchemaNode(c.Mapping(), name, on_completion,
        thanks_url, thanks_message, limit_by_date, message_before_start,
        message_after_end, start_date, end_date, validator=valid_interval)
    return public_link_schema


public_link_schema = create_public_link_schema()

