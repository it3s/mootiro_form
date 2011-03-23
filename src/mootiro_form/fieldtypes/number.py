# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.number_data import NumberData
from mootiro_form.models.field_option import FieldOption


class NumberField(FieldType):
    name = _('Number input')
    brief = _("An integer or a decimal number.")
    model = NumberData  # model for entry values

    defaultValue = dict(defaul='',
                        precision=0, # integer by default
                        separator='.',
                        required=False)

    def value(self, entry):
        data = sas.query(NumberData) \
                .filter(NumberData.field_id == self.field.id) \
                .filter(NumberData.entry_id == entry.id).first()

        return data.value if data else ''

    def get_schema_node(self):
        widget = d.widget.TextInputWidget(template='form_textinput')
        if self.field.required:
            sn = c.SchemaNode(c.Str(), title=self.field.label,
                name='input-{0}'.format(self.field.id), default=self.field.get_option('defaul'),
                description=self.field.description, widget=widget,
                )
        else:
            sn = c.SchemaNode(c.Str(), title=self.field.label,
                name='input-{0}'.format(self.field.id), default=self.field.get_option('defaul'),
                missing='',
                description=self.field.description, widget=widget,
                )

        return sn

    def save_data(self, entry, value):
        self.data = NumberData()
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
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])
        # decimal precision. If 0 then the number is an integer
        self.save_option('precision', int(options['precision']))
        # choose between '.' and ','
        self.save_option('separator', options['separator'])

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
            description=self.field.description,
            defaul=self.field.get_option('defaul'),
            precision=self.field.get_option('precision'),
            separator=self.field.get_option('separator'),
        )
        # Add to the dict all the options of this field
        d.update({o.option: o.value for o in self.field.options})
        return d
