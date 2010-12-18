# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, ForeignKey
from formcreator.models import Base

class FieldTemplate(Base):
    '''Represents a template of a form field.
    *label* is the text that appears next to the field, identifying it.
    *description* is a brief explanation.
    *help_text* is a long explanation.
    *title* is short content for a tooltip (HTML "title" attribute).
    *required* states whether filling in this field is mandatory.
    '''
    __tablename__ = "field_template"

    id = Column(Integer, Sequence('field_template_id_seq'), primary_key=True)
    label = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    help_text = Column(UnicodeText, nullable=False)
    title = Column(UnicodeText, nullable=False)
    required = Column(Boolean)
    type = Column(ForeignKey('field_type.id'))
    public = Column(Boolean)
