# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import colander as c
from mootiro_form import _
from mootiro_form.views import static_url
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
            _('Text contains {} words, the minimum is {}.') \
            .format(word_count, node.min_words))
    if word_count > node.max_words:
        raise c.Invalid(node,
            _('Text contains {} words, the maximum is {}.') \
            .format(word_count, node.max_words))
    return None


class FieldValidationError(Exception):
    '''Represents an error when validating a field while saving a form.
    '''
    def __init__(self, field_identification, errors):
        '''The first argument is a string that somehow identifies the field
        for the user to see in a pop up message.
        The second argument is the validation errors dictionary (for logging).
        '''
        self.id = field_identification
        self.errors = errors

    def __str__(self):
        return 'Validation error in a field: {}'.format(self.id)

    def get_log_message(self):
        return '{}\n{}\n'.format(unicode(self), repr(self.errors))


def validate_field(schema, data, id):
    try:
        return schema.deserialize(data)
    except c.Invalid as e:
        raise FieldValidationError(id, e.asdict())


class FieldType(object):
    '''Abstract base class for field types.

    Every subclass must implement:

    - a `name` string
    - a `brief` description string
    '''

    def __init__(self, field):
        '''`field` is the SQLAlchemy model.
        '''
        self.field = field

    def initJson(self):
        return ''

    '''Ao editar um form, adicionar um campo:
       -------------------------------------
    '''

    def get_widget(self):
        '''Returns a deform type, or deform-compatible type.
        Uses self.field.options (the model).
        '''
        raise NotImplementedError

    def validate_and_save(self, options):
        '''This is called when a form is being saved, with an argument
        `options` -- a dictionary originated from json input,
        representing all the data for this field.

        This method must first validate that data. If any validation errors are
        found, a FieldValidationError must be raised with one argument:
        a dictionary containing colander-like validation errors.

        The validation step is achieved by defining an *EditSchema* inner class
        in the simplest field types... or by overriding this method in the
        more complex ones.

        Secondly, this method must persist the data
        (usually done by the save_options() method).

        Finally, it may return a dictionary to be sent to the page as json,
        or it may return None.
        '''
        schema = self.edit_schema if hasattr(self, 'edit_schema') \
            else self.EditSchema()

        if hasattr(self, 'edit_schema'):
            schema = self.edit_schema
        else:
            schema = self.EditSchema()

        validate_field(schema, options,
            "{} #{}".format(self.name, self.field.id))
        self.save_basic_options(options)
        return self.save_options(options)

    def save_options(self, options):
        '''This method is not an API anymore, since we have validate_and_save().
        However, it is still provided here because the default implementation
        might be useful.
        '''
        for option, value in options.items():
            self.save_option(option, value)
        return None

    def save_basic_options(self, options):
        '''Persists the most common field properties.'''
        self.field.label  = options['label']
        self.field.rich    = options['rich']
        self.field.use_rich = options['use_rich']
        self.field.required  = options['required']
        self.field.position   = options['position']
        self.field.description = options['description']

    def save_option(self, option, value):
        '''Updates the value of a field option,
        or creates it if it doesn't exist.
        '''
        if not self.field.id:  # Solves bug of orphan options
            raise RuntimeError('Ops, save_option() while the field ID is {}' \
                .format(self.field.id))
        opt = sas.query(FieldOption).filter(FieldOption.option == option) \
                        .filter(FieldOption.field_id == self.field.id).first()
        if opt:
            opt.value = value
        else:
            sas.add(FieldOption(option=option, value=value, field=self.field))

    def to_dict(self, to_export=False):
        '''Default implementation that should work for most field types.'''
        d = self.base_dict()
        options = sas.query(FieldOption) \
                    .filter(FieldOption.field_id==self.field.id).all()
        d.update({o.option: o.value for o in options})
        return d

    def base_dict(self):
        return dict(
            type       =self.field.typ.name,
            label      =self.field.label,
            field_id   =self.field.id,
            required   =self.field.required,
            description=self.field.description,
            rich       =self.field.rich,
            use_rich   =self.field.use_rich,
        )

    def schema_options(self):
        '''Returns a schema node. Used by field_options_save() and
        field_options_form().
        '''
        raise NotImplementedError


    '''SEÇÃO JAVASCRIPT:
       ----------------
    '''

    def html_preview(self, field_options):
        '''Returns HTML.'''
        raise NotImplementedError

    def field_options_form(self, field_options):
        '''HTML do formulariozinho para o lado esquerdo.'''
        raise NotImplementedError


    '''Ao exibir um form, adicionar um campo ao schema (/form/view/id):
       -----------------------------------------------
    '''

    def get_schema_node(self, field_options):
        '''Returns a schema node.
        The argument is a model.
        '''
        raise NotImplementedError

    def _get_schema_node_args(self, defaul=False):
        '''Provides basic arguments to instantiate a SchemaNode. Intended to
        be used by subclasses when creating the schema node for the
        entry creation page.
        '''
        f = self.field
        kw = dict(title=f.label,
            name='input-{0}'.format(f.id),
            description=f.description,
            use_rich=f.use_rich,
            rich=f.rich,
            widget=self.get_widget(),
        )
        if not f.required:
            kw['missing'] = defaul
        if defaul:
            kw['defaul'] = f.get_option('defaul')
        return kw



    '''Ao salvar uma entry:
       -------------------
    '''

    def save_data(self, entry, val):
        '''Uses the models to persist the field data upon entry completion.
        val is the value from the validated form.
        '''
        self.data = TextData()
        self.data.field_id = self.field.id
        self.data.entry_id = entry.id
        self.data.value = val
        sas.add(self.data)


    '''Viewing entries:
       ---------------
    '''

    def get_data(self, entry):
        '''Para o campo 3 da entry 15... qual o valor resposta?
        Returns a python object (string, datetime, int etc.)
        (The field instance is in self.field.)
        '''
        raise NotImplementedError

    def script_url(self, request):
        '''Does not need to be overriden. Returns the virtual path to the
        javascript file that represents this field in the form edit screen.
        '''
        return static_url('mootiro_form:static/fieldtypes/{}/editing.js' \
            .format(type(self).__name__), request)

    def icon_url(self, request):
        '''Does not need to be overriden. Returns the virtual path to the
        icon that represents this field in the form edit screen.
        '''
        return static_url('mootiro_form:static/fieldtypes/{}/icon.png' \
            .format(type(self).__name__), request)


from mootiro_form.fieldtypes.text import TextField
from mootiro_form.fieldtypes.textarea import TextAreaField
from mootiro_form.fieldtypes.listfield import ListField
from mootiro_form.fieldtypes.datefield import DateField
from mootiro_form.fieldtypes.number import NumberField
from mootiro_form.fieldtypes.email import EmailField
from mootiro_form.fieldtypes.image import ImageField
from mootiro_form.models.field import Field, sas

all_fieldtypes = [TextField(Field()), TextAreaField(Field()),
                  EmailField(Field()), ListField(Field()),
                  DateField(Field()), NumberField(Field()),
                  ImageField(Field())]

fields_dict = {cls.__name__ : cls for cls in (TextField, TextAreaField,
               EmailField, ListField, DateField, NumberField, ImageField)}
