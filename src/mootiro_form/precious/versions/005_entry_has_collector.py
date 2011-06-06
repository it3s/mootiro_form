#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from migrate import *

meta = MetaData()


collector_table = Table('collector', meta,
    Column('id', Integer(), primary_key=True),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta,
        Column('id', Integer(), primary_key=True),
    )
    c = Column('collector_id', Integer, ForeignKey('collector.id'))
    # use_alter=True, name='fk_entry_collector_id'))
    t.append_column(c)  # in 0.7 this should be done before c.create()
    c.create(t, populate_default=True)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta,
        Column('id', Integer(), primary_key=True),
        Column('collector_id', Integer, ForeignKey('collector.id')),
    )
    t.c.collector_id.drop(bind=migrate_engine)

