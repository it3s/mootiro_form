# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column
from mootiro_web.user.models.user import User


class FormCategory(Base):
    '''Represents a category into which the user can file forms.'''
    __tablename__ = "form_category"
    id = id_column(__tablename__)
    name = Column(UnicodeText, nullable=False)  # TODO create index
    description = Column(UnicodeText, nullable=True)
    position = Column(Integer)

    user_id = Column(Integer, ForeignKey('user.id'))  # TODO create index
    user = relationship(User, backref=backref('categories', order_by=name,
                        cascade='all'))

    def __repr__(self):
        return "Category({},{},{},{})".format(self.name,self.description,
                                              self.position, self.user)

    def to_dict(self):
        return {'category_id': self.id,
                'category_name': self.name,
                'category_desc': self.description,
                'category_position': self.position,
                'forms': [form.to_dict() for form in self.forms]
                }
