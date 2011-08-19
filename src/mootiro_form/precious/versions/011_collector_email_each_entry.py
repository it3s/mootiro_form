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
    t = Table('collector', meta)
    c = Column('email_each_entry', Boolean(), default=False)
    t.append_column(c)
    c.create(t, populate_default=False)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('collector', meta)
    c = Column('email_each_entry', Boolean(), default=False)
    t.drop_column(c)
