# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field

from sqlalchemy import Column, Float, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref


class NumberData(Base):
    __tablename__ = "number_data"

    id = id_column(__tablename__)
    value = Column(Float, nullable=True)

    field_id = Column(Integer, ForeignKey('field.id'))
    entry_id = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry, backref=backref('number_data'))
    field = relationship(Field)

