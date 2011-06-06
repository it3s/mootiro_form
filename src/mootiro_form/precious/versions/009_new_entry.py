#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from migrate import *

meta = MetaData()

# Adds/removes boolean column "new" to the entry table to flag whether the user
# has seen an entry already or not. 
# Adds column 'new_entries' to the form table to count the amount of new entries.

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta)
    c = Column('new', Boolean(), default=True)
    t.append_column(c)
    c.create(t, populate_default=False)
    t = Table('form', meta)
    c = Column('new_entries', Integer(), default=0)
    t.append_column(c)
    c.create(t)

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    t = Table('entry', meta)
    c = Column('new', Boolean(), default=True)
    t.drop_column(c)
    t = Table('form', meta)
    c = Column('new_entries', Integer(), default=0)
    t.drop_column(c)

