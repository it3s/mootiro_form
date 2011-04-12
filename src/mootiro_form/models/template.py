# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Integer, ForeignKey
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column
from mootiro_form.models.template_font import TemplateFont

class Template(Base):
    '''Represents a visual template of a form.'''
    __tablename__ = "template"
    id = id_column(__tablename__)

    # colors
    background_color = Column(UnicodeText)
    header_color = Column(UnicodeText)
    form_color = Column(UnicodeText)
    tab_color = Column(UnicodeText)
    highlighted_field_color = Column(UnicodeText)
    help_color = Column(UnicodeText)

    # fonts
    title_font_id = Column(Integer, ForeignKey('template_font.id'))
    title_font = relationship(TemplateFont, single_parent=True,
                            primaryjoin=title_font_id,
                            backref=backref('template'),
                            cascade_backrefs='all,delete-orphan')
    subtitle_font_id = Column(Integer, ForeignKey('template_font.id'))
    subtitle_font = relationship(TemplateFont, single_parent=True,
                            primaryjoin=subtitle_font_id,
                            backref=backref('template'),
                            cascade_backrefs='all,delete-orphan')
#    tabs_font_id = Column(Integer, ForeignKey('template_font.id'))
#    tabs_font = relationship(TemplateFont, single_parent=True,
#                            backref=backref('template'),
#                            cascade_backrefs='all,delete-orphan')
#    form_font_id = Column(Integer, ForeignKey('template_font.id'))
#    form_font = relationship(TemplateFont, single_parent=True,
#                            backref=backref('template'),
#                            cascade_backrefs='all,delete-orphan')
#    help_font_id = Column(Integer, ForeignKey('template_font.id'))
#    help_font = relationship(TemplateFont, single_parent=True,
#                            backref=backref('template'),
#                            cascade_backrefs='all,delete-orphan')

    # system templates
    system_template_id = Column(Integer, unique=True, default=None)

    @property
    def system(self):
        return True if self.system_template_id else False

    def __repr__(self):
        return "Form Template (id = {0})".format(self.id)

    def __unicode__(self):
        return "Form Template (id = {0})".format(self.id)
