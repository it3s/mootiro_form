# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import colander as c
import deform as d
from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.text_data import TextData


class EmailField(FieldType):
    name = _('Email field')
    brief = _("email field")
    defaultValue = dict(defaul='', required=False)

    def get_widget(self):
        return d.widget.TextInputWidget(template='form_textinput')

    def value(self, entry):
        data = sas.query(TextData) \
                .filter(TextData.field_id == self.field.id) \
                .filter(TextData.entry_id == entry.id).first()
        return data.value if data else ''

    def get_schema_node(self):
        kw = self._get_schema_node_args(defaul=True)
        if not self.field.required:
            kw['missing'] = kw['defaul']
        kw['validator'] = c.Email(msg='Please enter a valid email address'
                                      ' such as "john.doe@domain.com".')
        return c.SchemaNode(c.Str(), **kw)

    def validate_and_save(self, options):
        # TODO: This method is here because EmailField currently has no
        # Python validation. To correct this, you have 2 options:
        # 1. Create an EditSchema inner class and delete this method,
        #    activating the superclass' method through inheritance.
        # 2. Simply implement this method differently if the above option is
        #    insufficient for this field's needs.
        self.save_basic_options(options)
        return self.save_options(options)

    def save_options(self, options):
        '''Persists specific field properties.'''
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])
