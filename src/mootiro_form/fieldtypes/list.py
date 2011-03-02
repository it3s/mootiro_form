# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.list_data import ListOption, ListData
from mootiro_form.models.field_option import FieldOption


class ListField(FieldType):
    name = _('List input')
    brief = _("List of options to select one or more.")
    model = ListData

    def value(self, entry):
        data = sas.query(ListData).join(ListOption) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListData.entry_id == entry.id).one()

        return data

    def get_schema_node(self):
        title = self.field.label
        values = sas.query(ListOption).filter(ListOption.field_id == self.field.id).all()

        # Get the type of list
        return c.SchemaNode(c.Integer(), title=title,
                        widget=d.widget.SelectWidget( \
                        values=tuple((v.value, v.label) for v in values)))

    def save_data(self, entry, value):
        self.data = ListData()
        # TODO: Check if is a valid value
        self.data.value = value
        self.data.entry_id = entry.id

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
