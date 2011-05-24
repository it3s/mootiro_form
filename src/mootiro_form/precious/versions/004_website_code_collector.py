#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()


website_code_collector = Table('website_code_collector', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('embed_frame_height', Integer())
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    website_code_collector.create(bind=migrate_engine)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    website_code_collector.drop(bind=migrate_engine)
