# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Integer, Sequence
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column


class FieldType(Base):
    '''Represents a kind of field that is possible in a form.
    *name* is the type's name.
    *description* is a brief explanation of the type.
    '''
    __tablename__ = "field_type"
    id = id_column(__tablename__)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
