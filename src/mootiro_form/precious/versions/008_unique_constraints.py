#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''http://packages.python.org/sqlalchemy-migrate/api.html

Be sure to read these:

http://www.postgresql.org/docs/8.4/static/indexes-unique.html

http://packages.python.org/sqlalchemy-migrate/api.html#migrate.changeset.constraint.UniqueConstraint


Para testar esta migration eu fiz este workflow:

# Voltar para o passado
git stash
git checkout 4d39f77d04daa9bd8718
# Criar o banco (dropdb && createdb)
mfr && ./devserver.sh
# migrate version_control ... 7
mfmist 7
# Voltar ao presente
git checkout indexes
git stash pop
# migrate upgrade ... 8
mfmiup 8

'''

from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()


form_template = Table('form_template', meta,
    Column('id', Integer(), primary_key=True),
)
form_template_font = Table('form_template_font', meta,
    Column('id', Integer(), primary_key=True),
    Column('template_id', Integer, ForeignKey('form_template.id')),
    Column('place', UnicodeText, nullable=False),
)
form_template_color = Table('form_template_color', meta,
    Column('id', Integer(), primary_key=True),
    Column('template_id', Integer, ForeignKey('form_template.id')),
    Column('place', UnicodeText, nullable=False),
)


indexes = [  # Index() is new in SQLAlchemy 0.7.
    Index('ix_form_template_font_template_id',
          form_template_font.c.template_id),
    Index('ix_form_template_color_template_id',
          form_template_color.c.template_id),
]
constraints = [
    UniqueConstraint('template_id', 'place', table=form_template_font, 
        name='form_template_font_template_id_place_key'),
    UniqueConstraint('template_id', 'place', table=form_template_color, 
        name='form_template_color_template_id_place_key')
]

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    for i in indexes:
        i.drop()
    # Substitute the indexes with composite unique constraints:
    for c in constraints:
        c.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    for i in indexes:
        i.create()
    for c in constraints:
        c.drop()

