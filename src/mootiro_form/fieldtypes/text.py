# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

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
        self.field.label = options['label']
        self.field.required = options['required'] == 'true'
        self.field.description = options['description']
        
        # Set the field position
        self.field.position = options['position']

        # Save default value
        self.save_option('default', options['defaul'])

    def save_option(self, option, value):
        opt = sas.query(FieldOption).filter(FieldOption.option == option) \
                       .filter(FieldOption.field_id == self.field.id).first()
        if opt:
            opt.value = value
        else:
            new_option = FieldOption(option, value)
            self.field.options.append(new_option)

    def schema_options(self):
        pass

    def to_json(self):
        typ = self.field.typ.js_proto_name
        field_id = self.field.id
        default = sas.query(FieldOption)\
                    .filter(FieldOption.field_id == field_id) \
                    .filter(FieldOption.option == 'default').first()
        return dict(
            field_id=field_id,
            label=self.field.label,
            type=typ,
            required=self.field.required,
            defaul=default.value if default else '',
            description=self.field.description,
        )
