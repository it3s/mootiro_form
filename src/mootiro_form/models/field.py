# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column, sas
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.form import Form

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref


class Field(Base):
    '''Represents a field of a form.
    *label* is the text that appears next to the field, identifying it.
    *description* is a brief explanation.
    *help_text* is a long explanation.
    *title* is short content for a tooltip (HTML "title" attribute).
    *position* is an integer for ordering fields inside the form.
    *required* states whether filling in this field is mandatory.
    *form_id* points to the form that owns this field.
    '''
    __tablename__ = "field"
    id = id_column(__tablename__)
    label = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    help_text = Column(UnicodeText, nullable=True)
    title = Column(UnicodeText, nullable=True)
    position = Column(Integer)
    required = Column(Boolean)

    typ_id = Column(ForeignKey('field_type.id'))
    typ = relationship(FieldType)

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('fields', order_by=position))

    def to_json(self):
        return fields_dict[self.typ.name](self).to_json()

    def save_option(self, option, value):
        return fields_dict[self.typ.name](self).save_option(option, value)

    def save_options(self, options_dict):
        return fields_dict[self.typ.name](self).save_options(options_dict)

    def get_option(self, option):
        opt = sas.query(FieldOption)\
                    .filter(FieldOption.field_id == self.id) \
                    .filter(FieldOption.option == option).first()

        if opt:
            return opt.value
        else:
            return fields_dict[self.typ.name](self).defaultValue[option]

    def value(self, entry):
        return fields_dict[self.typ.name](self).value(entry)

from mootiro_form.fieldtypes import all_fieldtypes, fields_dict
from mootiro_form.models.field_option import FieldOption
