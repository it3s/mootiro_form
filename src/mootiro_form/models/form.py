# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey, \
                       DateTime
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.formcategory import FormCategory
from mootiro_form.models.formtemplate import FormTemplate
from mootiro_form.models.user import User
from mootiro_form.models import sas


class Form(Base):
    '''Represents a form as created by a user.'''
    __tablename__ = "form"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created
    modified = now_column()  # when was this form saved
    name = Column(UnicodeText(255), nullable=False)
    submit_label = Column(UnicodeText(255))
    description = Column(UnicodeText)

    category_id = Column(Integer, ForeignKey('form_category.id'))
    category = relationship(FormCategory,
                            backref=backref('forms', order_by=name))

    template_id = Column(Integer, ForeignKey('form_template.id'))
    template = relationship(FormTemplate, backref=backref('forms',
                                    cascade='all'))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('forms', order_by=name,
                        cascade='all'))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '{0}. {1}'.format(self.id, self.name)

    @property
    def num_entries(self):
        num_entries = sas.query(Entry).filter(Entry.form_id == self.id).count()
        return num_entries

    def to_dict(self):
        return {'form_id': self.id,
                'form_name': self.name or 'Untitled form',
                'form_entries': self.num_entries,
                'form_description': self.description,
                # 'form_slug': self.slug,
                # 'form_public': self.public,
                # 'form_status': self.status,
                # 'form_thanks_message': self.thanks_message,
                'form_created': unicode(self.created)[:16],
                'form_modified': unicode(self.modified)[:16],
                'form_questions': sas.query(Field) \
                    .filter(Field.form_id == self.id).count()
        }

    def copy(self):
        form_copy = Form()

        # form instance copy
        for attr in ('user', 'category', 'name', 'template',  'description',
                'submit_label', 'thanks_message'):
            setattr(form_copy, attr, getattr(self, attr))
        # fields copy
        for f in self.fields:
            form_copy.fields.append(f.copy())

        sas.add(form_copy)

        return form_copy

from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field

