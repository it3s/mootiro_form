# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey, Enum
from sqlalchemy.orm import relationship, backref


class ListOption(Base):
    __tablename__ = "list_option"

    id = id_column(__tablename__)
    label = Column(UnicodeText())
    value = Column(UnicodeText())
    opt_default = Column(Boolean(), default=False)
    position = Column(Integer, default=0)
    status = Column(Enum('Approved', 'Rejected', 'Awaiting moderation',
                         'Form owner', name='list_option_status'))

    field_id = Column(Integer, ForeignKey('field.id'), index=True)
    field = relationship(Field, backref=backref('list_options',
                         cascade='all'))


class ListData(Base):
    __tablename__ = "list_data"
    id = id_column(__tablename__)

    value = Column(Integer, ForeignKey('list_option.id'), index=True)
    list_option = relationship(ListOption, backref='list_data')

    entry_id = Column(Integer, ForeignKey('entry.id'), index=True)
    entry = relationship(Entry, backref=backref('list_data'))

    field_id = Column(Integer, ForeignKey('field.id'), index=True)
    field = relationship(Field, backref=backref('list_data', cascade='all'))
