# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column


class TemplateFont(Base):
    '''Represents a font specification for visual form templates.'''
    __tablename__ = "template_font"
    id = id_column(__tablename__)

    name = Column(UnicodeText, nullable=False)
    size = Column(UnicodeText, nullable=False)
    bold = Column(Boolean, default=False)
    italic = Column(Boolean, default=False)
