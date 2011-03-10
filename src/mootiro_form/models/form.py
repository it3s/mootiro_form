# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.formcategory import FormCategory
from mootiro_form.models.user import User
from mootiro_form.models import sas


class Form(Base):
    '''Represents a form as created by a user.'''
    __tablename__ = "form"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created
    name = Column(UnicodeText(255), nullable=False)
    submit_label = Column(UnicodeText(255), nullable=True)
    description = Column(UnicodeText)
    public = Column(Boolean, default=False)
    slug = Column(UnicodeText(10))  # a part of the URL; 10 chars
    thanks_message = Column(UnicodeText(255))
    # answers = Column(Integer)

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
        num_entries = sas.query(Entry).filter(Entry.form_id == self.id).count()
        return num_entries

    def to_json(self):
        return {'form_id': self.id,
                'form_name': self.name or 'Untitled form',
                'form_entries': self.num_entries,
                'form_description': self.description,
                'form_slug': self.slug,
                'form_public': self.public,
                'form_thanks_message': self.thanks_message,
                'form_created': unicode(self.created)[:16],
        }


from mootiro_form.models.entry import Entry
