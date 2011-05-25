# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Float, Boolean, Integer, Sequence, ForeignKey, \
    Index
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field


class NumberData(Base):
    __tablename__ = "number_data"

    id = id_column(__tablename__)
    value = Column(Float, nullable=True)

    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship(Field, backref=backref('number_data', cascade='all'))

    entry_id = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry, backref=backref('number_data', cascade='all'))


# Create an index on 2 columns, for the query in class NumberField(FieldType)
number_field_entry_index = Index('ix_number_data_field_entry',
    NumberData.field_id, NumberData.entry_id)
