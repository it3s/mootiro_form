# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.text_data import TextData


class TextAreaField(FieldType):
    name = _('Text area')
    brief = _("Multiline text.")
    model = TextData

    defaultValue = dict(defaul='',
                        required=False)

    def value(self, entry):
        data = sas.query(TextData) \
                .filter(TextData.field_id == self.field.id) \
                .filter(TextData.entry_id == entry.id).first()
        return data.value if data else ''

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

    def save_options(self, options):
        self.field.label = options['label']
        self.field.required = options['required']
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

    def get_widget(self):
        return d.widget.TextAreaWidget(rows=5)

    def save_data(self, entry, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.entry_id = entry.id
        self.data.value = value
        sas.add(self.data)

    def to_json(self):
        field_id = self.field.id
        default = sas.query(FieldOption)\
                    .filter(FieldOption.field_id == field_id) \
                    .filter(FieldOption.option == 'default').first()
        return dict(
            field_id=field_id,
            label=self.field.label,
            type=self.field.typ.name,
            required=self.field.required,
            defaul=default.value if default else '',
            description=self.field.description,
        )
