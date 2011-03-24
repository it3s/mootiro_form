# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
from mootiro_form.views import static_url
from mootiro_form.models.field import Field, sas
from mootiro_form.models.field_option import FieldOption


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

    def field_options_save(self, field_options):
        '''Returns a Deform form object if there is a validation error.
        If validation passes... we are thinking, maybe already return the
        HTML with the new formatting for this field.

        The argument `field_options` is a structure originated from json input.
        '''
        raise NotImplementedError

    def save_options(self, options):
        for option, value in options.items():
            self.save_option(option, value)

    def save_option(self, option, value):
        '''Updates the value of a field option,
        or creates it if it doesn't exist.
        '''
        opt = sas.query(FieldOption).filter(FieldOption.option == option) \
                        .filter(FieldOption.field_id == self.field.id).first()
        if opt:
            opt.value = value
        else:
            sas.add(FieldOption(option=option, value=value, field=self.field))

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


    '''Ao salvar uma entry:
       -------------------
    '''

    model = None
    '''model é um atributo da classe que aponta para uma
    classe model (ex. DatetimeData).
    '''

    def save_data(self, val):
        '''Uses the model and persists.
        val is the value from the validated form.
        '''
        raise NotImplementedError


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

all_fieldtypes = [TextField(Field()), TextAreaField(Field()),
    ListField(Field()), DateField(Field()), NumberField(Field())]

fields_dict = {cls.__name__ : cls for cls in (TextField, TextAreaField, ListField, DateField, NumberField)}
