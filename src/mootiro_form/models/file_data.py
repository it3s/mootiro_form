# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Unicode, UnicodeText, Integer, \
                       ForeignKey, Index
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field


class FileData(Base):

    __tablename__ = "file_data"
    id = id_column(__tablename__)
    created = now_column()

    mimetype = Column(Unicode(255)) #http://tools.ietf.org/html/rfc4288#section-4.2
    filename = Column(UnicodeText)
    size = Column(Integer)
    path = Column(UnicodeText)
    thumbnail_path = Column(UnicodeText)

    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship(Field, backref=backref('file_data', cascade='all'))

    entry_id = Column(Integer, ForeignKey('entry.id'))
    entry = relationship(Entry, backref=backref('file_data', cascade='all'))

# Create an index on 2 columns, for the queries in text and email fieldtypes.
file_data_field_entry_index = Index('ix_file_data_field_entry',
    FileData.field_id, FileData.entry_id)

