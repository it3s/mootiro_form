# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form

from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship, backref


class Entry(Base):
    '''Represents a form entry.
    *created* is the moment the entry was created
    *form_id* points to the corresponding form.
    '''
    __tablename__ = "entry"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('entries', order_by=id))
