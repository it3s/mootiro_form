# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, DateTime, Integer, Sequence, ForeignKey
from formcreator.models import Base

class Entry(Base):
    '''Represents a form entry.
    *creation_datetime* is the datetime that the entry was created
    *form_id* points to the form that this entry belongs.
    '''
    __tablename__ = "entry"

    id = Column(Integer, Sequence('entry_id_seq'), primary_key=True)
    creation_datetime = Column(DateTime)
    form_id = Column(Integer, ForeignKey('form.id'))
