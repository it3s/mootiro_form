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
from mootiro_form.models.user import User
from mootiro_form.models.form import Form
from mootiro_form.models.field import Field
from mootiro_form.models.fieldtype import FieldType
from mootiro_form.models.fieldtemplate import FieldTemplate
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.entry import Entry
from mootiro_form.models.text_data import TextData
from mootiro_form.models.list_data import ListOption, ListData
from mootiro_form.models.date_data import DateData
from mootiro_form.models.formcategory import FormCategory
from mootiro_form.models.emailvalidationkey import EmailValidationKey
from mootiro_form.models.slugidentification import SlugIdentification
from mootiro_form.models.formtemplate import FormTemplate, FormTemplateFont, \
                                             FormTemplateColor

def create_test_data(settings):
    if not settings.get('create_test_data', False):
        return
    else:
        from mootiro_form.models.populate_data import insert_lots_of_data
        try:
            insert_lots_of_data(User.salt)
        except IntegrityError:
            sas.rollback()

def populate(settings):
    create_test_data(settings)
    if not settings.get('create_stravinsky', False):
        return
    session = sas()
    u = User(nickname='igor', real_name='Igor Stravinsky',
             email='stravinsky@geniuses.ru', password='igor',
             is_email_validated=True)
    session.add(u)

    # Create Field Types
    field_types_list = ['TextField', 'TextAreaField', 'ListField', 'DateField',
        'NumberField', 'EmailField']
    for typ in field_types_list:
        session.add(FieldType(typ))

    # Create Form System Templates

    # Template #1
    t1 = FormTemplate()
    t1.system_template_id = 1
    t1.colors.append(FormTemplateColor(place="background", hexcode="#F5E5C5"))
    t1.colors.append(FormTemplateColor(place="header", hexcode="#593D28"))
    t1.colors.append(FormTemplateColor(place="form", hexcode="#FFFFFF"))
    t1.colors.append(FormTemplateColor(place="tab", hexcode="#F2C2A7"))
    t1.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#93DEDB"))
    t1.colors.append(FormTemplateColor(place="help", hexcode="#B5F7F2"))
    t1.fonts.append(FormTemplateFont(place="title", name="Georgia", size=24, bold=True))
    t1.fonts.append(FormTemplateFont(place="subtitle", name="Myriad", size=14))
    t1.fonts.append(FormTemplateFont(place="tab", name="Myriad", size=9))
    t1.fonts.append(FormTemplateFont(place="form", name="Georgia", size=12))
    t1.fonts.append(FormTemplateFont(place="help", name="Myriad", size=10, italic=True))
    session.add(t1)

    # Template #4
    t4 = FormTemplate()
    t4.system_template_id = 4
    t4.colors.append(FormTemplateColor(place="background", hexcode="#68776C"))
    t4.colors.append(FormTemplateColor(place="header", hexcode="#00D6DD"))
    t4.colors.append(FormTemplateColor(place="form", hexcode="#E4FFE6"))
    t4.colors.append(FormTemplateColor(place="tab", hexcode="#B4EFB7"))
    t4.colors.append(FormTemplateColor(place="help", hexcode="#D4FF00"))
    t4.fonts.append(FormTemplateFont(place="title", name="Trebuchet", size=24, bold=True))
    t4.fonts.append(FormTemplateFont(place="subtitle", name="Trebuchet", size=14))
    t4.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t4.fonts.append(FormTemplateFont(place="form", name="Trebuchet", size=12))
    t4.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10, italic=True))
    session.add(t4)

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
