# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column, now_column, sas
from mootiro_form.models.field import Field


class FieldOption(Base):
    '''Represents a field option.'''
    __tablename__ = "field_option"
    id = id_column(__tablename__)
    option = Column(UnicodeText)
    value = Column(UnicodeText)
    field_id = Column(Integer, ForeignKey('field.id'), nullable=False)
    field = relationship(Field, backref=backref('options',
                         cascade='all, delete-orphan', single_parent=True))

    def __repr__(self):
        return "[{}. {} = {}]".format(self.id, self.option, self.value)

    def copy(self):
        field_option_copy = FieldOption()

        # field option instance copy
        for attr in ('option', 'value'):
            field_option_copy.__setattr__(attr, self.__getattribute__(attr))

        sas.add(field_option_copy)

        return field_option_copy