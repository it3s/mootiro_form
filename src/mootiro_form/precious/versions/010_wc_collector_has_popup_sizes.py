#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()
Base = declarative_base(metadata=meta)


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    class WebsiteCodeCollector(Base):
        __tablename__ = 'website_code_collector'
        __mapper_args__ = {'polymorphic_identity': 'website_code'}
        id = Column(Integer, ForeignKey('collector.id'), primary_key=True)

        invitation_message = Column(UnicodeText)
        embed_frame_height = Column(Integer)

    t = WebsiteCodeCollector.__table__
    c1 = Column('invitation_popup_width', Integer())
    t.append_column(c1)
    c1.create(t)
    c2 = Column('invitation_popup_height', Integer())
    t.append_column(c2)
    c2.create(t)


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    class WebsiteCodeCollector(Base):
        __tablename__ = 'website_code_collector'
        __mapper_args__ = {'polymorphic_identity': 'website_code'}
        id = Column(Integer, ForeignKey('collector.id'), primary_key=True)

        invitation_message = Column(UnicodeText)
        invitation_popup_width = Column(Integer)
        invitation_popup_height = Column(Integer)
        embed_frame_height = Column(Integer)

    t = WebsiteCodeCollector.__table__
    t.c.invitation_popup_width.drop()
    t.c.invitation_popup_height.drop()
