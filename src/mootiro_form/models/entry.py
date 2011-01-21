# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from datetime   import datetime
from sqlalchemy import Column, DateTime, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column
from .form import Form


class Entry(Base):
    '''Represents a form entry.
    *creation_datetime* is the moment the entry was created
    (automatically filled in by SQLAlchemy).
    *form_id* points to the corresponding form.
    '''
    __tablename__ = "entry"
    id = id_column(__tablename__)
    created = now_column() # when was this record created

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('entries', order_by=id))
