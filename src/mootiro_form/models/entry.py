# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime   import datetime

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form

from sqlalchemy import Column, DateTime, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class Entry(Base):
    '''Represents a form entry.
    *creation_datetime* is the moment the entry was created
    (automatically filled in by SQLAlchemy).
    *form_id* points to the corresponding form.
    '''
    __tablename__ = "entry"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('entries', order_by=id))
