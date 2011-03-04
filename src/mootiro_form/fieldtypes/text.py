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
    model = TextData  # model for entry values

    defaultValue = dict(defaul='', minLength=1, maxLength=500)

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
        '''Called by the form editor view in order to persist field properties.
        '''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])
        self.save_option('minLength', int(options['minLength']))
        self.save_option('maxLength', int(options['maxLength']))

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
            minLength=self.field.get_option('minLength'),
            maxLength=self.field.get_option('maxLength'),
        )
        # Add to the dict all the options of this field
        d.update({o.option: o.value for o in self.field.options})
        return d
