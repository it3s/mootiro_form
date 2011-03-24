# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.text_data import TextData


def min_and_max_words_validator(node, val):
    '''This is a colander validator that checks the number of words in the
    value.

    A colander validator is a callable which accepts two positional
    arguments: node and value. It returns None if the value is valid.
    It raises a colander.Invalid exception if the value is not valid.
    '''
    word_count = len(val.split())
    # TODO Pluralize these error messages
    if word_count < node.min_words:
        raise c.Invalid(node,
            _('Text contains {} words, but the minimum is {}.') \
            .format(word_count, node.min_words))
    if word_count > node.max_words:
        raise c.Invalid(node,
            _('Text contains {} words, but the maximum is {}.') \
            .format(word_count, node.max_words))
    return None


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
        if f.get_option('enableLength') == '1':
            validators.append(c.Length(min=int(f.get_option('minLength')),
                max=int(f.get_option('maxLength'))))
        if f.get_option('enableWords') == '1':
            kw['min_words'] = int(f.get_option('minWords'))
            kw['max_words'] = int(f.get_option('maxWords'))
            validators.append(min_and_max_words_validator)
        if validators:
            if len(validators) == 1:
                kw['validator'] = validators[0]
            else:
                kw['validator'] = c.All(*validators)
        return c.SchemaNode(c.Str(), **kw)

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
