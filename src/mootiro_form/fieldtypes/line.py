# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
from mootiro_form import _
from mootiro_form.fieldtypes import FieldType


class LineField(FieldType):
    name = _('Text line')
    brief = _("One line of text.")
