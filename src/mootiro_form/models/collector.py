# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey, \
                       DateTime, Unicode
from sqlalchemy.orm import relationship, backref, synonym
from mootiro_form.models import Base, id_column, sas
from mootiro_form.models.form import Form
from mootiro_form.utils.text import random_word


class Collector(Base):
    '''Represents a collector to collect form entries.'''
    __tablename__ = "collector"
    id = id_column(__tablename__)

    # Inheritance configuration
    typ = Column('type', UnicodeText(50))
    __mapper_args__ = {'polymorphic_on': typ}

    name = Column(UnicodeText(255), nullable=False)

    # When an entry is received, we can either display a thanks message,
    # or redirect to some URL. 3 columns are needed for this:
    thanks_message = Column(UnicodeText)
    thanks_url = Column(UnicodeText(2000))
    # We define on_completion as a property to validate its possible values:
    ON_COMPLETION_VALUES = ('msg', 'url')
    _on_completion = Column('on_completion', Unicode(3))
    @property
    def on_completion(self):
        return self._on_completion
    @on_completion.setter
    def on_completion(self, val):
        if val not in self.ON_COMPLETION_VALUES:
            raise ValueError \
                ('Invalid value for on_completion: "{0}"'.format(val))
        self._on_completion = val
    on_completion = synonym('_on_completion', descriptor=on_completion)
    # TODO: Replace synonym with SQLAlchemy 0.7 hybrid attribute

    limit_by_date = Column(Boolean, default=False)
    start_date     = Column(DateTime)
    end_date        = Column(DateTime)
    message_after_end = Column(UnicodeText)
    message_before_start = Column(UnicodeText)

    # When an instance is persisted, it automatically gets a slug,
    slug = Column(UnicodeText(10), nullable=False,  # a part of the URL.
        index=True, default=lambda: random_word(10))

    form_id = Column(Integer, ForeignKey('form.id'), index=True)
    form = relationship(Form, backref=backref('collectors', order_by=id,
        cascade='all'))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return 'Collector (id={0}, name="{1}")'.format(self.id, self.name)

    def to_dict(self):
        d = {k: getattr(self, k) for k in ('id', 'name', 'thanks_message',
            'thanks_url', 'on_completion', 'message_before_start',
            'message_after_end', 'limit_by_date', 'slug', 'status')}
        d['start_date'] = unicode(self.start_date)[:16] \
            if self.start_date else ''
        d['end_date'] = unicode(self.end_date)[:16] if self.end_date else ''
        d['type'] = self.typ
        d['display_type'] = self.typ.replace("_", " ").capitalize()
        return d

    STATUS_BEFORE = 'pending'  # before start date
    STATUS_DURING = 'published'  # entries may be created
    STATUS_AFTER = 'closed'  # after end date

    @property
    def status(self):
        '''Returns a status code.'''
        if (self.start_date and datetime.utcnow() < self.start_date
            and self.limit_by_date):
            return self.STATUS_BEFORE
        if (self.end_date and datetime.utcnow() > self.end_date
            and self.limit_by_date):
            return self.STATUS_AFTER
        return self.STATUS_DURING


class PublicLinkCollector(Collector):
    '''A collector that provides a slug based public link for collecting
    entries.

    We expect to add columns here in the future.
    '''
    __tablename__ = 'public_link_collector'
    __mapper_args__ = {'polymorphic_identity': 'public_link'}
    id = Column(Integer, ForeignKey('collector.id'), primary_key=True)


class WebsiteCodeCollector(Collector):
    '''A collector that provides slug based html codes for collecting entries
    inside external websites.

    We expect to add columns here in the future, also.
    '''
    __tablename__ = 'website_code_collector'
    __mapper_args__ = {'polymorphic_identity': 'website_code'}
    id = Column(Integer, ForeignKey('collector.id'), primary_key=True)

    embed_frame_height = Column(Integer)

    def to_dict(self):
        d = super(WebsiteCodeCollector, self).to_dict()
        d['embed_frame_height'] = self.embed_frame_height
        return d
