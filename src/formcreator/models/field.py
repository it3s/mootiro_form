# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, ForeignKey
from formcreator.models import Base

class Field(Base):
    '''Represents a field of a form.
    *label* is the text that appears next to the field, identifying it.
    *description* is a brief explanation.
    *help_text* is a long explanation.
    *title* is short content for a tooltip (HTML "title" attribute).
    *position* is an integer for ordering fields inside the form.
    *required* states whether filling in this field is mandatory.
    *form_id* points to the form that owns this field.
    '''
    __tablename__ = "field"

    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    label = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    help_text = Column(UnicodeText, nullable=False)
    title = Column(UnicodeText, nullable=False)
    position = Column(Integer)
    required = Column(Boolean)
    type = Column(ForeignKey('field_type.id'))
    form_id = Column(Integer, ForeignKey('form.id'))
