# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import colander as c
import deform as d
from mootiro_form import _
from mootiro_form.fieldtypes import FieldType, min_and_max_words_validator
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.text_data import TextData


def is_db_true(text):
    return text == '1' or text == 'true'


class TextBase(FieldType):
    '''Base class for both TextField and TextAreaField.'''
    model = TextData  # model for entry values

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
        validators = []
        if is_db_true(f.get_option('enableLength')):
            validators.append(c.Length(min=int(f.get_option('minLength')),
                max=int(f.get_option('maxLength'))))
        if is_db_true(f.get_option('enableWords')):
            kw['min_words'] = int(f.get_option('minWords'))
            kw['max_words'] = int(f.get_option('maxWords'))
            validators.append(min_and_max_words_validator)
        if validators:
            if len(validators) == 1:
                kw['validator'] = validators[0]
            else:
                kw['validator'] = c.All(*validators)
        return c.SchemaNode(c.Str(), **kw)

    def save_options(self, options):
        '''Called by the form editor view in order to persist field properties.
        '''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        # Save the other properties
        for s in self._special_options:
            self.save_option(s, options.get(s, ''))

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
        d['enableWords'] = is_db_true(d.get('enableWords', '0'))
        # d['enableLength'] = d['enableLength'] == '1'
        d['enableLength'] = is_db_true(d.get('enableLength', '0'))
        return d


class TextField(TextBase):
    name = _('Text input')
    brief = _("One line of text.")
    defaultValue = dict(defaul='', minLength=1, maxLength=500, required=False)

    def get_widget(self):
        return d.widget.TextInputWidget(template='form_textinput')

    _special_options = 'defaul enableLength minLength maxLength enableWords ' \
                 'minWords maxWords'.split()
