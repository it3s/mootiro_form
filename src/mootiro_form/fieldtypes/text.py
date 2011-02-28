# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import colander as c

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.text_data import TextData
from mootiro_form.models.field_option import FieldOption


class TextField(FieldType):
    typ = 'Text'
    name = _('Text input')
    brief = _("One line of text.")
    model = TextData

    def get_schema_node(self):
        return c.SchemaNode(c.Str(), title=self.field.label,
            name='input-{0}'.format(self.field.id), default='',
            description=self.field.description,
            **({} if self.field.required else {'missing': ''}))

    def save_data(self, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.value = value

    def save_options(self, options):
        for option, value in options.items():
            self.save_option(option, value)

    def save_option(self, option, value):
        new_option = FieldOption(option, value)
        self.field.options.append(new_option)

    def schema_options(self):
        pass

    def to_json(self):
        typ = self.field.typ.js_proto_name
        field_id = self.field.id
        field_label = self.field.label
        required = self.field.required
        default = sas.query(FieldOption)\
                    .filter(FieldOption.field_id == self.field.id)\
                    .filter(FieldOption.option == 'default').first()

        field_dict = dict([('field_id', field_id)
                          ,('label', field_label)
                          ,('type', typ)
                          ,('required', required)
                          ,('defaul', default.value)])

        return field_dict

