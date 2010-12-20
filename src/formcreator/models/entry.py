# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from datetime   import datetime
from sqlalchemy import Column, DateTime, Integer, Sequence, ForeignKey
from formcreator.models import Base

class Entry(Base):
    '''Represents a form entry.
    *creation_datetime* is the moment the entry was created
    (automatically filled in by SQLAlchemy).
    *form_id* points to the corresponding form.
    '''
    __tablename__ = "entry"

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    creation_datetime = Column(DateTime, default=datetime.utcnow)
    form_id = Column(Integer, ForeignKey('form.id'))
