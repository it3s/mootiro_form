#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()
Base = declarative_base(metadata=meta)


collector_table = Table('collector', meta,
    Column('id', Integer(), primary_key=True),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta,
        Column('id', Integer(), primary_key=True),
    )
    c = Column('collector_id', Integer, ForeignKey('collector.id'))
    c.create(t, populate_default=True)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta,
        Column('id', Integer(), primary_key=True),
        Column('collector_id', Integer, ForeignKey('collector.id')),
    )
    t.c.collector_id.drop(bind=migrate_engine)
