# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, ForeignKey, \
                       DateTime
from sqlalchemy.orm import relationship, backref
from mootiro_form.models import Base, id_column
from mootiro_form.models.form import Form


class Collector(Base):
    '''Represents a collector to collect form entries.'''
    __tablename__ = "collector"
    id = id_column(__tablename__)

    # Inheritance configuration
    typ = Column('type', UnicodeText(50))
    __mapper_args__ = {'polymorphic_on': typ}

    name = Column(UnicodeText(255), nullable=False)
    thanks_message = Column(UnicodeText)
    thanks_url = Column(UnicodeText(255))

    limit_by_date = Column(Boolean, default=False)
    # from then on the form will be accessible
    start_date = Column(DateTime, nullable=True)
    message_before_start = Column(UnicodeText)
    # until then the form will be accessible
    end_date = Column(DateTime, nullable=True)
    message_after_end = Column(UnicodeText)

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('collectors', order_by=id))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "Collector (id = {0}, name = {1})".format(self.id, self.name)


class PublicLinkCollector (Collector):
    '''A collector that provides a slug based public link for collecting
    entries.
    '''
    __tablename__ = 'public_link_collector'
    __mapper_args__ = {'polymorphic_identity': 'public_link'}
    id = Column(Integer, ForeignKey('collector.id'), primary_key=True)

    slug = Column(UnicodeText(10))  # a part of the URL; 10 chars
