#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()
Base = declarative_base(metadata=meta)


collector = Table('collector', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('type', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('thanks_message', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('thanks_url', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('on_completion', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('limit_by_date', Boolean(create_constraint=True, name=None)),
    Column('start_date', DateTime(timezone=False)),
    Column('end_date', DateTime(timezone=False)),
    Column('message_after_end', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('message_before_start', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('slug', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('form_id', Integer()),
)


public_link_collector = Table('public_link_collector', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    # 1. Create the collectors tables
    collector.create(bind=migrate_engine)
    public_link_collector.create(bind=migrate_engine)

    # Finally, delete columns from the Form table
    class Form(Base):
        __tablename__ = "form"
        id = Column(Integer, primary_key=True, nullable=False)
        created = Column(DateTime(timezone=False),  nullable=False)
        modified = Column(DateTime(timezone=False),  nullable=False)
        # from then on the form will be accessible
        start_date = Column(DateTime)
        # until then the form will be accessible
        end_date = Column(DateTime)
        name = Column(UnicodeText(255), nullable=False)
        submit_label = Column(UnicodeText(255))
        description = Column(UnicodeText)
        public = Column(Boolean, default=False)
        slug = Column(UnicodeText(10))  # a part of the URL; 10 chars
        thanks_message = Column(UnicodeText(255))
        category_id = Column(Integer, ForeignKey('form_category.id'))
        template_id = Column(Integer, ForeignKey('form_template.id'))
        user_id = Column(Integer, ForeignKey('user.id'))
    t = Form.__table__
    t.c.start_date.drop()
    t.c.end_date.drop()
    t.c.public.drop()
    t.c.thanks_message.drop()
    t.c.slug.drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    # 1. Drop the collectors tables
    public_link_collector.drop(bind=migrate_engine)
    collector.drop(bind=migrate_engine)

    # Finally, add columns to the Form table
    class Form(Base):
        __tablename__ = "form"
        id = Column(Integer, primary_key=True, nullable=False)
        created = Column(DateTime(timezone=False),  nullable=False)
        modified = Column(DateTime(timezone=False),  nullable=False)
        name = Column(UnicodeText(255), nullable=False)
        submit_label = Column(UnicodeText(255))
        description = Column(UnicodeText)
        category_id = Column(Integer, ForeignKey('form_category.id'))
        template_id = Column(Integer, ForeignKey('form_template.id'))
        user_id = Column(Integer, ForeignKey('user.id'))
    t = Form.__table__
    sd = Column('start_date', DateTime(timezone=False))
    ed = Column('end_date', DateTime(timezone=False))
    p = Column('public', Boolean(), default=False)
    tm = Column('thanks_message', UnicodeText(255))
    s = Column('slug', UnicodeText(10))
    sd.create(t)
    ed.create(t)
    p.create(t, populate_default=True)
    tm.create(t)
    s.create(t)
