# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref


class ListOption(Base):
    __tablename__ = "list_option"

    id = id_column(__tablename__)
    label = Column(UnicodeText())
    value = Column(UnicodeText())
    opt_default = Column(Boolean(), default=False)
    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship(Field)

class ListData(Base):
    __tablename__ = "list_data"

    id = id_column(__tablename__)
    value = Column(Integer, ForeignKey('list_option.id'))
    entry_id = Column(Integer, ForeignKey('entry.id'))
    field_id =  Column(Integer, ForeignKey('field.id'))
    entry = relationship(Entry, backref=backref('list_data'))
    list_option = relationship(ListOption, backref=('list_data'))
