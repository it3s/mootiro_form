# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, Unicode, Integer, Sequence
from formcreator.models import Base

class User(Base):
    '''Represents a user of the application: someone who creates forms.'''
    __tablename__ = "user"
    id = Column(Integer, Sequence(__tablename__ + '_id_seq'), primary_key=True)
    username = Column(Unicode, nullable=False, unique=True)
    name = Column(Unicode)
    password_hash = Column(Unicode)
    email = Column(Unicode)

