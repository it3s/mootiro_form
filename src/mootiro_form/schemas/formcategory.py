# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from mootiro_form import _
from mootiro_form.models import sas, FormCategory


# Minimum and maximum lengths
# ==========================

LEN_NAME = dict(min=1,)
LEN_DESCRIPTION = dict(min=1,)

# Classes
# =======
#class NewCategorySchema(c.MappingSchema):
#    name = c.SchemaNode(c.Str(), title=_('Name  '),
#            validator=c.Length(**LEN_NAME))
#    description = c.SchemaNode(c.Str(), title=_('Description'), missing='',
#            validator=c.Length(**LEN_DESCRIPTION))
#
# Imperatively built Schema
# =========================

def create_category_schema(user):
    '''Returns a  schema for creation of a category, imperatively built'''
    schema = c.SchemaNode(c.Mapping())
    schema.add(c.SchemaNode(c.Str(), name="name", title=_('Name'),
             validator=c.All(c.Length(**LEN_NAME),
                 validate_based_on_user(user))))

    schema.add(c.SchemaNode(c.Str(), name="description", title=_('Description'),
               missing='', validator=c.Length(**LEN_DESCRIPTION)))
    
    return schema

def validate_based_on_user(user):
    def validate_user(node, value):
        cat = sas.query(FormCategory) \
                .filter(FormCategory.user_id==user.id) \
                .filter(FormCategory.name==value).all()
        if cat:
            raise c.Invalid(node, _('There is a category with that name'))
    return validate_user
