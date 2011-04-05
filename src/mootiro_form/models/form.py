# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey, \
                       DateTime
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
    modified = now_column()  # when was this form saved
    # from then on the form will be accessible 
    start_date = Column(DateTime, nullable=True)
    # until then the form will be accessible
    end_date = Column(DateTime, nullable=True)
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
    user = relationship(User, backref=backref('forms', order_by=name))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{0}. {1}'.format(self.id, self.name)

    @property
    def num_entries(self):
        num_entries = sas.query(Entry).filter(Entry.form_id == self.id).count()
        return num_entries

    STATUS_EDITING = 'editing' # form is not public yet
    STATUS_BEFORE = 'before'  # form is public but before start date
    STATUS_DURING = 'during'  # form is public and entries may be created
    STATUS_AFTER = 'after'  # form is public but after end date

    @property
    def status(self):
        '''Returns a form status code.'''
        if not self.public:
            return self.STATUS_EDITING
        if self.start_date and datetime.utcnow() < self.start_date:
            return self.STATUS_BEFORE
        if self.end_date and datetime.utcnow() > self.end_date:
            return self.STATUS_AFTER
        return self.STATUS_DURING

    def to_dict(self):
        return {'form_id': self.id,
                'form_name': self.name or 'Untitled form',
                'form_entries': self.num_entries,
                'form_description': self.description,
                'form_slug': self.slug,
                'form_public': self.public,
                'form_status': self.status,
                'form_thanks_message': self.thanks_message,
                'form_created': unicode(self.created)[:16],
                'form_modified': unicode(self.modified)[:16],
                'form_questions': sas.query(Field) \
                    .filter(Field.form_id == self.id).count()
                    # len(self.fields),
        }

    def copy(self):
        form_copy = Form()

        # form instance copy
        for attr in ('user', 'category', 'name', 'description',
                'submit_label', 'thanks_message'):
            form_copy.__setattr__(attr, self.__getattribute__(attr))
        # fields copy
        for f in self.fields:
            form_copy.fields.append(f.copy())

        sas.add(form_copy)
        sas.flush()

        return form_copy

from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field
