# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey, Index
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field


class TextData(Base):
    __tablename__ = "text_data"

    id = id_column(__tablename__)
    value = Column(UnicodeText, nullable=True)

    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship(Field, backref=backref('text_data', cascade='all'))

    entry_id = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry, backref=backref('text_data', cascade='all'))


# Create an index on 2 columns, for the queries in text and email fieldtypes.
text_data_field_entry_index = Index('ix_text_data_field_entry',
    TextData.field_id, TextData.entry_id)
