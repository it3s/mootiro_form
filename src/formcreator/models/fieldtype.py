# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Integer, Sequence
from formcreator.models import Base

class FieldType(Base):
    '''The types os field possible in a form.
    *name* is the type's name
    *description* is a brief explanation of the type.
    '''
    __tablename__ = "field_type"

    id = Column(Integer, Sequence('field_type_id_seq'), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
