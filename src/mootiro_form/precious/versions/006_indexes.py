#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Be sure to read these:

http://www.postgresql.org/docs/8.4/static/indexes-unique.html

http://packages.python.org/sqlalchemy-migrate/api.html#migrate.changeset.constraint.UniqueConstraint


Para testar esta migration eu fiz este workflow:

# Voltar para o passado
git stash
git checkout 4d39f77d04daa9bd8718
# Criar o banco (dropdb && createdb)
mfr && ./devserver.sh
# migrate version_control ... 5
mfmist 5
# Voltar ao presente
git checkout indexes
git stash pop
# migrate upgrade ... 6
mfmiup 6

'''

from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()


user_table = Table('user', meta,
    Column('id', Integer(),  primary_key=True),
    Column('email', Unicode(255), nullable=False, unique=True),
    Column('nickname', Unicode(32), nullable=False, unique=True),
    Column('password_hash', Unicode(40), nullable=False),
)
slug_id = Table('slug_identification', meta,
    Column('id', Integer(), primary_key=True),
    Column('user_slug', Unicode(10), nullable=False, unique=True),
)
evk = Table('email_validation_key', meta,
    Column('id', Integer(), primary_key=True),
    Column('key', Unicode(20), nullable=False, unique=True),
    Column('user_id', Integer, ForeignKey('user.id')),
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
field_option = Table('field_option', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id'), nullable=False),
    Column('option', UnicodeText),
)
form_template = Table('form_template', meta,
    Column('id', Integer(), primary_key=True),
    Column('system_template_id', Integer, unique=True, default=None),
)
form_template_font = Table('form_template_font', meta,
    Column('id', Integer(), primary_key=True),
    Column('template_id', Integer, ForeignKey('form_template.id')),
)
form_template_color = Table('form_template_color', meta,
    Column('id', Integer(), primary_key=True),
    Column('template_id', Integer, ForeignKey('form_template.id')),
)
text_data = Table('text_data', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
    Column('entry_id', Integer, ForeignKey('entry.id')),
)
date_data = Table('date_data', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
    Column('entry_id', Integer, ForeignKey('entry.id')),
)
number_data = Table('number_data', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
    Column('entry_id', Integer, ForeignKey('entry.id')),
)
list_option = Table('list_option', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
)
list_data = Table('list_data', meta,
    Column('id', Integer(), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id')),
    Column('entry_id', Integer, ForeignKey('entry.id')),
    Column('value', Integer, ForeignKey('list_option.id')),
)


# DO NOT create indexes on columns that have unique=True:
    #Index('ix_user_email', user_table.c.email, unique=True),
    #Index('ix_user_nickname', user_table.c.nickname, unique=True),
    #Index('ix_slug_identification_user_slug', slug_id.c.user_slug, unique=True),
    #Index('ix_email_validation_key_key', evk.c.key, unique=True),
    #Index('ix_form_template_system_template_id',
    #      form_template.c.system_template_id, unique=True),


indexes = [  # Index() is new in SQLAlchemy 0.7.
    Index('ix_user_password_hash', user_table.c.password_hash),
    Index('ix_email_validation_key_user_id', evk.c.user_id),
    Index('ix_form_user_id', form_table.c.user_id),
    Index('ix_collector_form_id', collector_table.c.form_id),
    Index('ix_entry_form_id', entry_table.c.form_id),
    Index('ix_entry_collector_id', entry_table.c.collector_id),
    Index('ix_field_form_id', field_table.c.form_id),
    Index('ix_form_template_font_template_id',
          form_template_font.c.template_id),
    Index('ix_form_template_color_template_id',
          form_template_color.c.template_id),
    Index('ix_list_option_field_id', list_option.c.field_id),
    Index('ix_list_data_value', list_data.c.value),
    Index('ix_list_data_field_id', list_data.c.field_id),
    Index('ix_list_data_entry_id', list_data.c.entry_id),
    # Composite indexes:
    Index('ix_field_option_field_option',
        field_option.c.field_id, field_option.c.option),
    Index('ix_date_data_field_entry',
        date_data.c.field_id, date_data.c.entry_id),
    Index('ix_number_data_field_entry',
        number_data.c.field_id, number_data.c.entry_id),
    Index('ix_text_data_field_entry',
        text_data.c.field_id, text_data.c.entry_id),
]


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    for i in indexes:
        i.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    for i in indexes:
        i.drop()
