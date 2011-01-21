# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column
from .formcategory import FormCategory
from .auth import User


class Form(Base):
    '''Represents a form as created by a user.'''
    __tablename__ = "form"
    id = id_column(__tablename__)
    created = now_column() # when was this record created
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText)
    public = Column(Boolean)
    slug = Column(UnicodeText) # a part of the URL; 10 chars

    category_id = Column(Integer, ForeignKey('form_category.id'))
    category = relationship(FormCategory,
                            backref=backref('forms', order_by=name))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User,
                        backref=backref('forms', order_by=name))
