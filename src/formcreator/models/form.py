# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, ForeignKey
from formcreator.models import Base

class Form(Base):
    '''Represents a form as created by a user.'''
    __tablename__ = "form"
    
    id = Column(Integer, Sequence('form_id_seq'), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText)
    public = Column(Boolean)
    url = Column(UnicodeText)
    category_id = Column(Integer, ForeignKey('form_category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

