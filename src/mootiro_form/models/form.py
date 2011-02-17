# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.formcategory import FormCategory
from mootiro_form.models.user import User
from mootiro_form.models import sas
from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class Form(Base):
    '''Represents a form as created by a user.'''
    __tablename__ = "form"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText)
    public = Column(Boolean)
    slug = Column(UnicodeText)  # a part of the URL; 10 chars
#    answers = Column(Integer)

    category_id = Column(Integer, ForeignKey('form_category.id'))
    category = relationship(FormCategory,
                            backref=backref('forms', order_by=name))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User,
                        backref=backref('forms', order_by=name))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{0}. {1}'.format(self.id, self.name)

    @property
    def num_entries(self):
        from mootiro_form.models.entry import Entry
        num_entries = sas.query(Entry).filter(Entry.form_id == self.id).count()
        return num_entries
