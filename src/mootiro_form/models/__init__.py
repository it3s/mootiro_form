# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

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


# Functions that help defining our models
# =======================================

def id_column(tablename, typ=Integer):
    return Column(typ, Sequence(tablename + '_id_seq'), primary_key=True)


def now_column(nullable=False):
    return Column(DateTime, default=datetime.utcnow, nullable=nullable)


def get_col(model, name):
    '''Introspects the SQLALchemy model `model` and returns the column object
    for the column named `name`. E.g.: col(User, 'email')
    '''
    cols = model._sa_class_manager.mapper.columns
    return cols[name]


def _get_length(col):
    return None if col is None else getattr(col.type, 'length', None)


def get_length(model, field):
    '''Returns the length of column `field` of a SQLAlchemy model `model`.'''
    return _get_length(get_col(model, field))


def col(attrib):
    '''Given a sqlalchemy.orm.attributes.InstrumentedAttribute
    (type of the attributes of model classes),
    returns the corresponding column. E.g.: col(User.email)
    '''
    return attrib.property.columns[0]


def length(attrib):
    '''Returns the length of the attribute `attrib`.'''
    return _get_length(col(attrib))

# class Base(object):
#    length_of = classmethod(get_length)
Base = declarative_base()  # (cls=Base)


# Import all models here
from .user import User
from .form import Form
from .field import Field
from .fieldtype import FieldType
from .fieldtemplate import FieldTemplate
from .entry import Entry
from .textinput_data import TextInputData
from .formcategory import FormCategory
from .emailvalidationkey import EmailValidationKey
from .slugidentification import SlugIdentification

def populate(settings):
    if not settings.get('create_stravinsky', False):
        return
    session = sas()
    u = User(nickname='igor', real_name='Igor Stravinsky',
             email='stravinsky@geniuses.ru', password='igor',
             is_email_validated=True)
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
