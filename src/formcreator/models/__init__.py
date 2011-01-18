# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

import transaction
from datetime import datetime
from sqlalchemy import create_engine, Column, Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, DateTime
from zope.sqlalchemy import ZopeTransactionExtension

sas = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


# Functions that help defining our models
# =======================================

def id_column(tablename, typ=Integer):
    return Column(typ, Sequence(tablename + '_id_seq'), primary_key=True)

def now_column(nullable=False):
    return Column(DateTime, default=datetime.utcnow, nullable=nullable)


# Import all models here
from formcreator.models.auth import User # , Group
from formcreator.models.form import Form
from formcreator.models.field import Field
from formcreator.models.fieldtype import FieldType
from formcreator.models.fieldtemplate import FieldTemplate
from formcreator.models.entry import Entry
from formcreator.models.formcategory import FormCategory


def populate(settings):
    if not settings.get('create_stravinsky', False):
        return
    session = sas()
    u = User(nickname='igor', real_name='Igor Stravinsky', email='stravinsky@it3s.org', password='igor')
    session.add(u)
    session.flush()
    transaction.commit()

def initialize_sql(engine, db_echo=False, settings={}):
    sas.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate(settings)
    except IntegrityError:
        sas.rollback()
        # pass
