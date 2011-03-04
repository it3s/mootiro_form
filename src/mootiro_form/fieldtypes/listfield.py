# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.list_data import ListOption, ListData
from mootiro_form.models.field_option import FieldOption


class ListField(FieldType):
    name = _('List input')
    brief = _("List of options to select one or more.")
    model = ListData

    defaultValue = dict(defaul='',
                        list_type='select',
                        required=False)

    def value(self, entry):
        data = sas.query(ListData).join(ListOption) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListData.entry_id == entry.id).one()

        return data.list_option.label if data else ''

    def get_schema_node(self):
        title = self.field.label
        values = sas.query(ListOption).filter(ListOption.field_id == self.field.id).all()

        # Get the type of list
        return c.SchemaNode(c.Str(), title=title,
                        name='input-{0}'.format(self.field.id),
                        widget=d.widget.SelectWidget(
                        values=tuple((v.id, v.label) for v in values)))

    def save_data(self, entry, value):
        self.data = ListData()
        # TODO: Check if is a valid value
        self.data.value = value
        self.data.entry_id = entry.id
        self.data.field_id = self.field.id
        sas.add(self.data)

    def save_options(self, options):
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']

        # Set the field position
        self.field.position = options['position']

        # Save default value
        self.save_option('default', options['defaul'])

        # List Type
        self.save_option('list_type', options['list_type'])

        for list_option in options['options']:
            if list_option['id'] != 'new':
                lo = sas.query(ListOption).get(list_option['id'])
                lo.label = list_option['label']
                lo.value = list_option['value']
            elif list_option['label'] != '':
                lo = ListOption()
                lo.label = list_option['label']
                lo.value = list_option['value']
                lo.field = self.field
                sas.add(lo)

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
        list_optionsObj = sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id).all()

        list_options = [{'label':lo.label, 'value':lo.value, 'id':lo.id} \
                                        for lo in list_optionsObj]

        return dict(
            field_id=field_id,
            label=self.field.label,
            type=self.field.typ.name,
            list_type=self.field.get_option('list_type'),
            options=list_options,
            required=self.field.required,
            defaul=self.field.get_option('defaul'),
            description=self.field.description,
        )
