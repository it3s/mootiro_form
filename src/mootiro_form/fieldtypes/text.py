# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.text_data import TextData
from mootiro_form.models.field_option import FieldOption


class TextField(FieldType):
    name = _('Text input')
    brief = _("One line of text.")
    model = TextData

    def value(self, entry):
        data = sas.query(TextData) \
                .filter(TextData.field_id == self.field.id) \
                .filter(TextData.entry_id == entry.id).one()
        return data.value

    def get_schema_node(self):
        widget = d.widget.TextInputWidget(template='form_textinput')
        sn = c.SchemaNode(c.Str(), title=self.field.label,
            name='input-{0}'.format(self.field.id), default='',
            description=self.field.description, widget=widget,
            )
        return sn

    def save_data(self, entry, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.entry_id = entry.id
        self.data.value = value
        sas.add(self.data)

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
