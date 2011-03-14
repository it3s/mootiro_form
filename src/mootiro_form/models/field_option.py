# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column, sas
from mootiro_form.models.field import Field

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref


class FieldOption(Base):
    '''Represents a field option.
    '''
    __tablename__ = "field_option"
    id = id_column(__tablename__)
    option = Column(UnicodeText, nullable=True)
    value = Column(UnicodeText, nullable=True)
    field_id = Column(Integer, ForeignKey('field.id'))
    field = relationship(Field, backref=backref('options'))

    def __init__(self, option, value):
        self.option = option
        self.value = value

