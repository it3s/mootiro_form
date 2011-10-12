# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid.decorator import reify
from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column, now_column, sas
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.form import Form


class Field(Base):
    '''Represents a field of a form.
    *label* is the text that appears next to the field, identifying it.
    *description* is a brief explanation.
    *rich* may contain a rich text alternative to both *label* and
    *description* together.
    *use_rich* is a flag that determines which alternative is to be used.
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
    rich = Column(UnicodeText, nullable=False, default='')
    use_rich = Column(Boolean, default=False)
    help_text = Column(UnicodeText, nullable=True)
    title    = Column(UnicodeText, nullable=True)
    position = Column(Integer)
    required = Column(Boolean)

    typ_id = Column(ForeignKey('field_type.id'))  # TODO: index?
    typ = relationship(FieldType)

    form_id = Column(Integer, ForeignKey('form.id'), index=True)
    form = relationship(Form, backref=backref('fields', order_by=position,
                                              cascade='all'))

    def __repr__(self):
        return '{} #{} "{}"{}'.format(self.typ.name, self.id, self.label,
            '*' if self.required else '')

    @reify
    def fieldtype(self):
        return fields_dict[self.typ.name](self)

    def to_dict(self, to_export=False):
        d = self.fieldtype.to_dict(to_export=to_export)
        return d

    def save_option(self, option, value):
        return self.fieldtype.save_option(option, value)

    def save_options(self, options_dict):
        return self.fieldtype.save_options(options_dict)

    def validate_and_save(self, props):
        return self.fieldtype.validate_and_save(props)

    def get_option(self, option):
        opt = sas.query(FieldOption)\
                    .filter(FieldOption.field_id == self.id) \
                    .filter(FieldOption.option == option).first()
        if opt:
            return opt.value
        else:
            return self.fieldtype.defaultValue[option]

    def value(self, entry):
        return self.fieldtype.value(entry)

    copy_props = 'label description rich use_rich help_text title position ' \
                 'required typ'.split()
    def copy(self):
        field_copy = Field()
        # field instance copy
        for attr in self.copy_props:
            field_copy.__setattr__(attr, self.__getattribute__(attr))
        # field options copy
        for o in self.options:
            field_copy.options.append(o.copy())
        # field specific options copy
        fieldtype = fields_dict[self.typ.name](field_copy)
        if getattr(fieldtype, 'copy', None):
            fieldtype.copy(self)
        sas.add(field_copy)
        return field_copy


from mootiro_form.fieldtypes import all_fieldtypes, fields_dict
from mootiro_form.models.field_option import FieldOption
