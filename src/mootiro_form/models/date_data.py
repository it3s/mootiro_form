# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field

from sqlalchemy import Column, Date, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref


class DateData(Base):
    __tablename__ = "date_data"

    id = id_column(__tablename__)
    value = Column(Date, nullable=True)

    field_id = Column(Integer, ForeignKey('field.id'))
    entry_id = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry, backref=backref('date_data'))
    field = relationship(Field)


