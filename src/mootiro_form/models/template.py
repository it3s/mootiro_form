# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column

class Template(Base):
    '''Represents a visual template of a form.'''
    __tablename__ = "template"
    id = id_column(__tablename__)

    # system templates
    system_template_id = Column(Integer, unique=True, default=None)
    @property
    def system(self):
        return True if self.system_template_id else False

    def __repr__(self):
        return "Form Template (id = {0})".format(self.id)

    def __unicode__(self):
        return self.__repr__()


class TemplateFont(Base):
    '''Represents a font specification for visual form templates.'''
    __tablename__ = "template_font"
    id = id_column(__tablename__)

    place = Column(UnicodeText, nullable=False)
    name = Column(UnicodeText, nullable=False)
    size = Column(UnicodeText, nullable=False)
    bold = Column(Boolean, default=False)
    italic = Column(Boolean, default=False)

    template_id = Column(Integer, ForeignKey('template.id'))
    template = relationship(Template, backref=backref('fonts'),
                            cascade_backrefs='all,delete-orphan')

    def __unicode__(self):
        style = ""
        style += " bold " if self.bold else ""
        style += " italic " if self.italic else ""
        return "{0} {1} {2}".format(self.name, self.size, style)

    def __repr__(self):
        return "TemplateFont: {0} = {1}".format(self.place, self.__unicode__())


class TemplateColor(Base):
    '''Represents a color specification for visual form templates.'''
    __tablename__ = "template_color"
    id = id_column(__tablename__)

    place = Column(UnicodeText, nullable=False)
    hexcode = Column(UnicodeText, nullable=False)

    template_id = Column(Integer, ForeignKey('template.id'))
    template = relationship(Template, backref=backref('colors'),
                            cascade_backrefs='all,delete-orphan')

    def __unicode__(self):
        return self.hexcode

    def __repr__(self):
        return "TemplateColor: {0} = {1}".format(self.place, self.__unicode__())