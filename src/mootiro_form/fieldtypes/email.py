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
        f = self.field
        defaul = f.get_option('defaul')
        kw = dict(title=f.label,
            name='input-{0}'.format(f.id),
            default=defaul,
            description=f.description,
            widget=self.get_widget(),
        )
        if not f.required:
            kw['missing'] = defaul
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
        return self.save_options(options)

    def save_options(self, options):
        '''Persists field properties.'''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        # Save the other properties
        self.save_option('defaul', options['defaul'])

    def to_dict(self, to_export=False):
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
        return d



