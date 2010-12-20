# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from formcreator.models import Base

class FormCategory(Base):
    '''Represents a category into which the user can file forms.'''
    __tablename__ = "form_category"
    
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    position = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
