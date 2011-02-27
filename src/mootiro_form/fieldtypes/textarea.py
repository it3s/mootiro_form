# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models.text_data import TextData


class TextAreaField(FieldType):
    typ = 'TextArea'
    name = _('Text area')
    brief = _("Multiline text.")
    model = TextData

    def get_schema_node(self):
        return c.SchemaNode(c.Str(), title=self.field.label,
            name='input-{0}'.format(self.field.id), default='',
            description=self.field.description,
            widget=self.get_widget(),
            **({} if self.field.required else {'missing': ''}))

    def save_data(self, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.value = value

    def get_widget(self):
        return d.widget.TextAreaWidget(rows=5)

    def save_data(self, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.value = value

    def to_json(self):
        typ = self.field.typ.js_proto_name
        field_id = self.field.id
        field_label = self.field.label
        required = self.field.required

        field_dict = dict([('field_id', field_id)
                          ,('label', field_label)
                          ,('type', typ)
                          ,('required', required)])

        return field_dict

