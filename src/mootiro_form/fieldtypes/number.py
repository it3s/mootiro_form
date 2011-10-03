from __future__ import unicode_literals

import colander as c
import deform as d
from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.number_data import NumberData


class NumberField(FieldType):
    name = _('Number input')
    brief = _("number field")

    defaultValue = dict(defaul='',
                        precision=0, # integer by default
                        separator='.',
                        prefix='',
                        suffix='',
                        required=False)

    def value(self, entry):
        data = sas.query(NumberData) \
                .filter(NumberData.field_id == self.field.id) \
                .filter(NumberData.entry_id == entry.id) \
                .first()

        if not data:
            return ''

        value = unicode(data.value)

        prec = int(self.field.get_option('precision'))
        sep = self.field.get_option('separator')
        if prec != 0:
            if value.split('.')[1] == "0":
                value = value.split('.')[0]
            elif sep == ',':
                value = value.replace('.', ',')
        else:
            # convert to integer string
            value = value.split('.')[0]

        prefix = self.field.get_option('prefix')
        if prefix != '':
            value = prefix + ' ' + value
        suffix = self.field.get_option('suffix')
        if suffix != '':
            value = value + ' ' + suffix

        return value

    def get_widget(self):
        return d.widget.TextInputWidget(template='form_number')

    def get_schema_node(self):
        f = self.field
        params = self._get_schema_node_args(defaul=False)
        precision = int(f.get_option('precision'))
        separator = f.get_option('separator')

        params['default'] = f.get_option('defaul')
        if separator == ',':
            params['default'] = params['default'].replace('.', ',')

        if not f.required:
            params['missing'] = ''

        if precision == 0:
            params['validator'] = get_validator('integer')
        else:
            params['validator'] = get_validator('decimal', separator=separator,
                                    precision=precision)

        params['prefix'] = f.get_option('prefix')
        params['suffix'] = f.get_option('suffix')
        return c.SchemaNode(c.Str(), **params)

    def save_data(self, entry, value):
        if value != '':
            value = value.replace(',', '.')
            self.data = NumberData()
            self.data.field_id = self.field.id
            self.data.entry_id = entry.id
            self.data.value = value
            sas.add(self.data)

    def validate_and_save(self, options):
        # TODO: This method is here because NumberField currently has no
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
        # decimal precision. If 0 then the number is an integer
        self.save_option('precision', int(options['precision']))
        # choose between '.' and ','
        self.save_option('separator', options['separator'])
        self.save_option('prefix', options['prefix'])
        self.save_option('suffix', options['suffix'])

    def schema_options(self):
        pass

# Validators
def get_validator(type, **kw):
    if type == 'integer':
        def integer_validator(node, value):
            v = unicode(value)

            try:
                x = float(v.replace(',', '.'))
            except ValueError:
                raise c.Invalid(node, _('Please enter a number.'))
            # if needed, at this point x is the float value to be saved.

            if v.find('.') != -1 or v.find(',') != -1:
                raise c.Invalid(node, _('Please enter an integer number.'))
        validator = integer_validator

    elif type == 'decimal':
        def decimal_validator(node, value):
            v = unicode(value)
            sep = kw['separator']
            prec = kw['precision']

            try:
                x = float(v.replace(',', '.'))
            except ValueError:
                raise c.Invalid(node, _('Please enter a number.'))
            # if needed, at this point x is the float value to be saved.

            if (sep == '.' and v.find(',') != -1) or \
               (sep == ',' and v.find('.') != -1):
                raise c.Invalid(node, _('Wrong separator. Try swapping dot (.) and comma (,).'))

            try:
                dec = v.split(sep)[1] # capture decimal part
            except IndexError:
                return None # validation succeeded

            if len(dec) > prec:
                raise c.Invalid(node, \
                    _("Maximum of %(p)d decimals.") % {'p': prec})

        validator = decimal_validator
    return validator
