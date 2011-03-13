# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.date_data import DateData
from mootiro_form.models.field_option import FieldOption

from datetime import datetime

class DateField(FieldType):
    name = _('Date input')
    brief = _("Select a simple date")

    defaultValue = dict(defaul='',
                        date_format='%Y-%m-%d',
                        export_date_format='%Y-%m-%d',
                        required=False)

    def value(self, entry):
        date_format = self.field.get_option('date_format')
        data = sas.query(DateData) \
                .filter(DateData.field_id == self.field.id) \
                .filter(DateData.entry_id == entry.id).first()
        return data.value.strftime(date_format) if data else ''

    def get_schema_node(self):
        widget = d.widget.DateInputWidget(template='form_date')
        if self.field.required:
            sn = c.SchemaNode(c.Date(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                default=datetime.strptime(self.field.get_option('defaul'),
                                        self.field.get_option('date_format')),
                description=self.field.description, widget=widget,
                )
        else:
            sn = c.SchemaNode(c.Date(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                default=datetime.strptime(self.field.get_option('defaul'),
                                        self.field.get_option('date_format')),
                missing=c.null,
                description=self.field.description, widget=widget,
                )

        return sn

    def save_data(self, entry, value):
        if value != c.null:
            self.data = DateData()
            self.data.field_id = self.field.id
            self.data.entry_id = entry.id
            self.data.value = value
            sas.add(self.data)

    def save_options(self, options):
        '''Called by the form editor view in order to persist field properties.
        '''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        self.save_option('input_date_format', options['input_date_format'])
        self.save_option('export_date_format', options['export_date_format'])
#        self.field.position = options['export_date_format']
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])

    def save_option(self, option, value):
        '''Updates or creates the value of a field option.'''
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
        d = dict(
            type=self.field.typ.name,
            label=self.field.label,
            field_id=self.field.id,
            required=self.field.required,
            input_data_format=self.field.get_option('date_format'),
            export_data_format=self.field.get_option('export_date_format'),
            description=self.field.description,
            defaul=self.field.get_option('defaul'),
        )
        # Add to the dict all the options of this field
        d.update({o.option: o.value for o in self.field.options})
        return d
