# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column
from .user import User


class FormCategory(Base):
    '''Represents a category into which the user can file forms.'''
    __tablename__ = "form_category"
    id = id_column(__tablename__)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    position = Column(Integer)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('categories', order_by=name))
