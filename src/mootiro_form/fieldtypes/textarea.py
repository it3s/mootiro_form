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

    def get_widget(self):
        return d.widget.TextAreaWidget(rows=5)

    def save_data(self, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.value = value

    def to_json(self):
        typ = self.field.typ.name
        field_id = self.field.id
        field_label = self.field.label
        required = self.field.required

        field_dict = dict([('field_id', field_id)
                          ,('label', field_label)
                          ,('type', typ)
                          ,('required', required)])

        return field_dict
