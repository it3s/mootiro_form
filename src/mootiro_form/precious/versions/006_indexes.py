#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()


user_table = Table('user', meta,
    Column('id', Integer(),  primary_key=True),
)
form_table = Table('form', meta,
    Column('id', Integer(), primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
)
collector_table = Table('collector', meta,
    Column('id', Integer(), primary_key=True),
    Column('form_id', Integer, ForeignKey('form.id')),
)
entry_table = Table('entry', meta,
    Column('id', Integer(), primary_key=True),
    Column('form_id', Integer, ForeignKey('form.id')),
    Column('collector_id', Integer, ForeignKey('collector.id')),
)
field_table = Table('field', meta,
    Column('id', Integer(), primary_key=True),
    Column('form_id', Integer, ForeignKey('form.id')),
)
date_data = Table('date_data', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
    Column('entry_id', Integer, ForeignKey('entry.id')),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    # "Index" is new in SQLAlchemy 0.7.
    Index('ix_form_user_id', form_table.c.user_id).create()
    Index('ix_collector_form_id', collector_table.c.form_id).create()
    Index('ix_entry_form_id', entry_table.c.form_id).create()
    Index('ix_entry_collector_id', entry_table.c.collector_id).create()
    Index('ix_field_form_id', field_table.c.form_id).create()
    Index('ix_date_data_field_id', date_data.c.field_id).create()
    Index('ix_date_data_entry_id', date_data.c.entry_id).create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    Index('ix_form_user_id', form_table.c.user_id).drop()
    Index('ix_collector_form_id', collector_table.c.form_id).drop()
    Index('ix_entry_form_id', entry_table.c.form_id).drop()
    Index('ix_entry_collector_id', entry_table.c.collector_id).drop()
    Index('ix_field_form_id', field_table.c.form_id).drop()
    Index('ix_date_data_field_id', date_data.c.field_id).drop()
    Index('ix_date_data_entry_id', date_data.c.entry_id).drop()
