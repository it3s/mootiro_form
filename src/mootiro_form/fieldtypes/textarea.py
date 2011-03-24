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

    defaultValue = dict(defaul='', required=False)

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

    _special_options = 'defaul enableLength minLength maxLength enableWords ' \
                 'minWords maxWords height width'.split()

    def save_options(self, options):
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        # Save the other properties
        for s in self._special_options:
            self.save_option(s, options[s])

    def get_widget(self):
        return d.widget.TextAreaWidget(rows=5)

    def save_data(self, entry, value):
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.entry_id = entry.id
        self.data.value = value
        sas.add(self.data)

    def to_dict(self):
        field_id = self.field.id
        d = dict(
            type=self.field.typ.name,
            label=self.field.label,
            field_id=field_id,
            required=self.field.required,
            description=self.field.description,
        )
        options = sas.query(FieldOption) \
                      .filter(FieldOption.field_id == field_id).all()
        d.update({o.option: o.value for o in options})
        # d['enableWords'] = d['enableWords'] == '1'
        d['enableWords'] = d.get('enableWords', '0') == '1'
        # d['enableLength'] = d['enableLength'] == '1'
        d['enableLength'] = d.get('enableLength', '0') == '1'
        return d
