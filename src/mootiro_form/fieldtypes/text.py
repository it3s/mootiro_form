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

def sub_raise(node, subnode, msg):
    e = c.Invalid(node)
    e[subnode] = msg
    raise e

def validate_length(node, val):
    if val['minLength'] > val['maxLength']:
        sub_raise(node, 'minLength', 'Higher than max length')

def validate_words(node, val):
    if val['minWords'] > val['maxWords']:
        sub_raise(node, 'minWords', 'Higher than max words')

def validate_defaul_length(node, val):
    lendefaul = len(val['defaul'])
    if lendefaul and val['enableLength']:
        if val['minLength'] > lendefaul:
            sub_raise(node, 'defaul', 'Shorter than min length')
        if val['maxLength'] < lendefaul:
            sub_raise(node, 'defaul', 'Longer than max length')

def validate_defaul_words(node, val):
    word_count = len(val['defaul'].split())
    if word_count and val['enableWords']:
        if val['minWords'] > word_count:
            sub_raise(node, 'defaul', 'Shorter than min words')
        if val['maxWords'] < word_count:
            sub_raise(node, 'defaul', 'Longer than max words')


class TextBase(FieldType):
    '''Base class for both TextField and TextAreaField.'''

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
            use_rich=f.use_rich,
            rich=f.rich,
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

    # Validation schema

    class EditSchema(c.MappingSchema):
        '''Inner class for validating user input from the form editor.'''
        defaul = c.SchemaNode(c.Str(), missing='')
        enableWords = c.SchemaNode(c.Bool())
        enableLength = c.SchemaNode(c.Bool())
        minLength = c.SchemaNode(c.Int(), validator=c.Range(min=1),
            missing=1)
        maxLength = c.SchemaNode(c.Int(), validator=c.Range(min=1),
            missing=800)
        minWords = c.SchemaNode(c.Int(), validator=c.Range(min=1), missing=1)
        maxWords = c.SchemaNode(c.Int(), validator=c.Range(min=1), missing=400)

    edit_schema = EditSchema(validator=c.All(validate_length, validate_words,
        validate_defaul_length, validate_defaul_words))

    def save_options(self, options):
        '''Persists specific field properties.'''
        for s in self._special_options:
            self.save_option(s, options.get(s, ''))

    def to_dict(self, to_export=False):
        d = super(TextBase, self).to_dict(to_export=to_export)
        d['enableWords'] = is_db_true(d.get('enableWords', '0'))
        d['enableLength'] = is_db_true(d.get('enableLength', '0'))
        return d


class TextField(TextBase):
    name = _('Text input')
    brief = _("single line of text")
    defaultValue = dict(defaul='', minLength=1, maxLength=500, required=False)

    def get_widget(self):
        return d.widget.TextInputWidget(template='form_textinput')

    _special_options = 'defaul enableLength minLength maxLength enableWords ' \
                 'minWords maxWords'.split()
