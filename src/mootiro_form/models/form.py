# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json

from sqlalchemy import Column, UnicodeText, Integer, ForeignKey, Index
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
    description = Column(UnicodeText)
    submit_label = Column(UnicodeText(255))
    # Incremented number of the last entry. Serves as a counter of the entries
    last_entry_number = Column(Integer, default=0)
    # How many new entries since last visit
    new_entries = Column(Integer, default=0)

    # TODO: Create an index here when categories make their triumphant comeback
    category_id = Column(Integer, ForeignKey('form_category.id'))
    category = relationship(FormCategory,
                            backref=backref('forms', order_by=name))

    # TODO: Create an index here if we ever query from the parent
    template_id = Column(Integer, ForeignKey('form_template.id'))
    template = relationship(FormTemplate, backref=backref('forms',
                            cascade='all'))

    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user = relationship(User, backref=backref('forms', order_by=name,
                        cascade='all'))

    STATUS_EDITION = "edition"
    STATUS_PENDING = "pending"
    STATUS_PUBLISHED = "published"
    STATUS_CLOSED = "closed"

    @property
    def status(self):
        from mootiro_form.models.collector import Collector

        collectors_status = (Collector.STATUS_DURING, Collector.STATUS_BEFORE,
            Collector.STATUS_AFTER)

        classifier = {}
        for cs in collectors_status:
            classifier[cs] = []
        for c in self.collectors:
            classifier[c.status].append(c)

        if classifier[Collector.STATUS_DURING]:
            status = self.STATUS_PUBLISHED
            num_colls_in_status = len(classifier[Collector.STATUS_DURING])
        elif classifier[Collector.STATUS_BEFORE]:
            status = self.STATUS_PENDING
            num_colls_in_status = len(classifier[Collector.STATUS_BEFORE])
        elif classifier[Collector.STATUS_AFTER]:
            status = self.STATUS_CLOSED
            num_colls_in_status = len(classifier[Collector.STATUS_AFTER])
        else:
            status = self.STATUS_EDITION
            num_colls_in_status = 0

        return (status, num_colls_in_status)

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
                'form_new_entries': self.new_entries,
                'form_description': self.description,
                'form_created': unicode(self.created)[:16],
                'form_modified': unicode(self.modified)[:16],
                'form_status': self.status[0],
                'form_status_num': self.status[1],
                'form_questions': sas.query(Field) \
                    .filter(Field.form_id == self.id).count()
        }

    def export_json(self):
        form_dict = dict(form_name=self.name or 'Untitled form',
                         form_description=self.description,
                         fields=[f.to_dict(to_export=True) for f in self.fields])

        for field in form_dict['fields']:
            field.pop('field_id')

        return json.dumps(form_dict, indent=4)

    def copy(self):
        form_copy = Form()

        # form instance copy
        for attr in ('user', 'category', 'name', 'template',  'description',
                'submit_label'):
            setattr(form_copy, attr, getattr(self, attr))
        # fields copy
        for f in self.fields:
            form_copy.fields.append(f.copy())

        sas.add(form_copy)

        return form_copy


from mootiro_form.models.entry import Entry
from mootiro_form.models.field import Field
