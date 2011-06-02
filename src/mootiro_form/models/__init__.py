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
from mootiro_form.models.collector import Collector, PublicLinkCollector
from mootiro_form.models.entry import Entry
from mootiro_form.models.text_data import TextData
from mootiro_form.models.list_data import ListOption, ListData
from mootiro_form.models.date_data import DateData
from mootiro_form.models.formcategory import FormCategory
from mootiro_form.models.emailvalidationkey import EmailValidationKey
from mootiro_form.models.slugidentification import SlugIdentification
from mootiro_form.models.formtemplate import FormTemplate, FormTemplateFont, \
                                             FormTemplateColor


def create_test_data(options):
    if options.pop('create', 'false').lower() == 'true':
        from mootiro_form.models.populate_test_data import insert_lots_of_data
        insert_lots_of_data(**options)


def populate_fieldtypes():
    # Create Field Types
    field_types_list = ['TextField', 'TextAreaField', 'ListField', 'DateField',
        'NumberField', 'EmailField']
    for typ in field_types_list:
        sas.add(FieldType(name=typ))
    transaction.commit()  # so next functions will see these data

def populate_system_templates():
    # Template #1
    t = FormTemplate()
    t.system_template_id = 1
    t.system_template_name = "default"
    t.colors.append(FormTemplateColor(place="background", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#ffffff"))
    t.fonts.append(FormTemplateFont(place="title", name="Trebuchet", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Trebuchet", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Trebuchet", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Trebuchet", size=10))
    sas.add(t)

    # Template #2
    t = FormTemplate()
    t.system_template_id = 2
    t.system_template_name = "pacific"
    t.colors.append(FormTemplateColor(place="background", hexcode="#fcfff5"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#3e606f"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#91aa9d"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#dfe5cf"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#d1dbbd"))
    t.fonts.append(FormTemplateFont(place="title", name="Tahoma", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Tahoma", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Tahoma", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Tahoma", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Tahoma", size=10))
    sas.add(t)

    # Template #3
    t = FormTemplate()
    t.system_template_id = 3
    t.system_template_name = "spring"
    t.colors.append(FormTemplateColor(place="background", hexcode="#ffc0a9"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#fc6b86"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#7d8a2e"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#e9f2ad"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#c9d787"))
    t.fonts.append(FormTemplateFont(place="title", name="Verdana", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Verdana", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Verdana", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Verdana", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10))
    sas.add(t)

    # Template #4
    t = FormTemplate()
    t.system_template_id = 4
    t.system_template_name = "pool"
    t.colors.append(FormTemplateColor(place="background", hexcode="#68776c"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#00d6dd"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#e4ffe6"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#b4efb7"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#d4ff00"))
    t.fonts.append(FormTemplateFont(place="title", name="Trebuchet", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Trebuchet", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Trebuchet", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10, italic=True))
    sas.add(t)

    # Template #5
    t = FormTemplate()
    t.system_template_id = 5
    t.system_template_name = "stone"
    t.colors.append(FormTemplateColor(place="background", hexcode="#f5e5c5"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#593d28"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#f2c2a7"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#93dedb"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#b5f7f2"))
    t.fonts.append(FormTemplateFont(place="title", name="Georgia", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Myriad", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Myriad", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Georgia", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Myriad", size=10, italic=True))
    sas.add(t)

    # Template #6
    t = FormTemplate()
    t.system_template_id = 6
    t.system_template_name = "fog"
    t.colors.append(FormTemplateColor(place="background", hexcode="#7d9392"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#a7a37e"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#046380"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#efecca"))
    t.fonts.append(FormTemplateFont(place="title", name="Times", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Times", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Times", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Times", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Times", size=10, italic=True))
    sas.add(t)

    # Template #7
    t = FormTemplate()
    t.system_template_id = 7
    t.system_template_name = "garden"
    t.colors.append(FormTemplateColor(place="background", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#b0cc99"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#f9efcf"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#7c995e"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#ddd2c7"))
    t.fonts.append(FormTemplateFont(place="title", name="Georgia", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Georgia", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Georgia", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Georgia", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10, italic=True))
    sas.add(t)

    # Template #8
    t = FormTemplate()
    t.system_template_id = 8
    t.system_template_name = "plum"
    t.colors.append(FormTemplateColor(place="background", hexcode="#e6b098"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#8e4a64"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#f9edd4"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#cc4452"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#efacb6"))
    t.fonts.append(FormTemplateFont(place="title", name="Georgia", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Georgia", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Georgia", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10, italic=True))
    sas.add(t)

    # Template #9
    t = FormTemplate()
    t.system_template_id = 9
    t.system_template_name = "winter"
    t.colors.append(FormTemplateColor(place="background", hexcode="#cbe7e6"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#009a93"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#89ccca"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#ffd3b6"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#fc9f60"))
    t.fonts.append(FormTemplateFont(place="title", name="Trebuchet", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Trebuchet", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Trebuchet", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10))
    sas.add(t)

    # Template #10
    t = FormTemplate()
    t.system_template_id = 10
    t.system_template_name = "sand"
    t.colors.append(FormTemplateColor(place="background", hexcode="#fbf7e4"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#a83d4a"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#b4efb7"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#d3ceaa"))
    t.fonts.append(FormTemplateFont(place="title", name="Helvetica", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Helvetica", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Helvetica", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Helvetica", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Helvetica", size=10, italic=True))
    sas.add(t)

    # Template #11
    t = FormTemplate()
    t.system_template_id = 11
    t.system_template_name = "autumn"
    t.colors.append(FormTemplateColor(place="background", hexcode="#695d46"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#ff712c"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#fff6c5"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#cfc291"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#a1e8d9"))
    t.fonts.append(FormTemplateFont(place="title", name="Trebuchet", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Trebuchet", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Trebuchet", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Trebuchet", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Georgia", size=10))
    sas.add(t)

    # Template #12
    t = FormTemplate()
    t.system_template_id = 12
    t.system_template_name = "summer"
    t.colors.append(FormTemplateColor(place="background", hexcode="#f5e5c5"))
    t.colors.append(FormTemplateColor(place="header", hexcode="#826049"))
    t.colors.append(FormTemplateColor(place="form", hexcode="#ffffff"))
    t.colors.append(FormTemplateColor(place="tab", hexcode="#9d9d9c"))
    t.colors.append(FormTemplateColor(place="highlighted_field", hexcode="#fff599"))
    t.colors.append(FormTemplateColor(place="help", hexcode="#b5f7f2"))
    t.fonts.append(FormTemplateFont(place="title", name="Helvetica", size=24, bold=True))
    t.fonts.append(FormTemplateFont(place="subtitle", name="Helvetica", size=14))
    t.fonts.append(FormTemplateFont(place="tab", name="Helvetica", size=9))
    t.fonts.append(FormTemplateFont(place="form", name="Helvetica", size=12))
    t.fonts.append(FormTemplateFont(place="help", name="Helvetica", size=10))
    sas.add(t)


def initialize_sql(engine, db_echo=False, settings={}, prefix='testdata.'):
    sas.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    options = {key[len(prefix):]: val for key, val in settings.items() \
        if key.startswith(prefix)}
    try:
        populate_fieldtypes()
        transaction.begin()
        populate_system_templates()
        sas.flush()
        create_test_data(options)
    except IntegrityError:
        transaction.abort()
    else:
        transaction.commit()

