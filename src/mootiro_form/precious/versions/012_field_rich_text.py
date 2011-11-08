#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *


meta = MetaData()
Base = declarative_base(metadata=meta)

t = Table('field', meta)
delta = [
    # http://code.google.com/p/sqlalchemy-migrate/issues/detail?id=102
    Column('rich', UnicodeText, default=''),
    Column('use_rich', Boolean, default=False),
]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    for col in delta:
        t.append_column(col)
        col.create(t, populate_default=True)
    # After column "rich" is created and populated, add NOT NULL to it
    # (migrate really should do this automatically. Bummer.)
    sql = "ALTER TABLE field ALTER COLUMN rich SET NOT NULL;"
    connection = migrate_engine.connect()
    result = connection.execute(sql)
    # print(result)
    connection.close()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    for col in delta:
        t.drop_column(col)
