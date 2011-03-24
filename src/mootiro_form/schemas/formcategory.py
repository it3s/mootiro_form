# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from mootiro_form import _

# Minimum and maximum lengths
# ==========================

LEN_NAME = dict(min=1,)
LEN_DESCRIPTION = dict(min=1,)

# Classes
# =======
class NewCategorySchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(), title=_('Name  '),
            validator=c.Length(**LEN_NAME))
    description = c.SchemaNode(c.Str(), title=_('Description'), missing='',
            validator=c.Length(**LEN_DESCRIPTION))
