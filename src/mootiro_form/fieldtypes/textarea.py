# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models.text_data import TextData


class TextAreaField(FieldType):
    name = _('Text area')
    brief = _("a text block.")
    typ = 'TextArea'
    model = TextData

    def get_schema_node(self):
        return c.SchemaNode(c.Str(), title=self.field.label,
                    name='input-{0}'.format(self.field.id),
                    default='',
                    description=self.field.description,
                    widget=self.get_widget(),
                    **({} if self.field.required else {'missing': ''})
                    )

    def get_widget(self):
        return d.widget.TextAreaWidget(rows=5)

    def save_data(self, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.value = value

