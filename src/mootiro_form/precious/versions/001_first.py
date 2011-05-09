from sqlalchemy import *
from migrate import *


from sqlalchemy import *
meta = MetaData()


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

date_data = Table('date_data', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('value', Date()),
    Column('field_id', Integer()),
    Column('entry_id', Integer()),
)

email_validation_key = Table('email_validation_key', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('key', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('generated_on', DateTime(timezone=False),  nullable=False),
    Column('user_id', Integer()),
)

entry = Table('entry', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('created', DateTime(timezone=False),  nullable=False),
    Column('entry_number', Integer()),
    Column('form_id', Integer()),
)

field = Table('field', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('label', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('description', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('help_text', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('title', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('position', Integer()),
    Column('required', Boolean(create_constraint=True, name=None)),
    Column('typ_id', Integer()),
    Column('form_id', Integer()),
)

field_option = Table('field_option', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('option', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('value', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('field_id', Integer(),  nullable=False),
)

field_template = Table('field_template', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('label', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('description', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('help_text', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('title', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('required', Boolean(create_constraint=True, name=None)),
    Column('type', Integer()),
    Column('public', Boolean(create_constraint=True, name=None)),
)

field_type = Table('field_type', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('description', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

form = Table('form', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('created', DateTime(timezone=False),  nullable=False),
    Column('modified', DateTime(timezone=False),  nullable=False),
    Column('name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('submit_label', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('description', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('category_id', Integer()),
    Column('template_id', Integer()),
    Column('user_id', Integer()),
)

form_category = Table('form_category', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('description', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('position', Integer()),
    Column('user_id', Integer()),
)

form_template = Table('form_template', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('system_template_id', Integer()),
    Column('system_template_name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

form_template_color = Table('form_template_color', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('place', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('hexcode', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('template_id', Integer()),
)

form_template_font = Table('form_template_font', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('place', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('name', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('size', Integer(),  nullable=False),
    Column('bold', Boolean(create_constraint=True, name=None)),
    Column('italic', Boolean(create_constraint=True, name=None)),
    Column('template_id', Integer()),
)

list_data = Table('list_data', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('value', Integer()),
    Column('entry_id', Integer()),
    Column('field_id', Integer()),
)

list_option = Table('list_option', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('label', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('value', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('opt_default', Boolean(create_constraint=True, name=None)),
    Column('position', Integer()),
    Column('status', Enum()),
    Column('field_id', Integer()),
)

number_data = Table('number_data', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('value', Float(precision=None, asdecimal=False)),
    Column('field_id', Integer()),
    Column('entry_id', Integer()),
)

public_link_collector = Table('public_link_collector', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
)

slug_identification = Table('slug_identification', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('user_slug', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('created', DateTime(timezone=False),  nullable=False),
    Column('user_id', Integer()),
)

text_data = Table('text_data', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('value', Text(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('field_id', Integer()),
    Column('entry_id', Integer()),
)

user = Table('user', meta,
    Column('id', Integer(),  primary_key=True, nullable=False),
    Column('created', DateTime(timezone=False),  nullable=False),
    Column('changed', DateTime(timezone=False),  nullable=False),
    Column('nickname', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('real_name', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('email', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
    Column('newsletter', Boolean(create_constraint=True, name=None)),
    Column('is_email_validated', Boolean(create_constraint=True, name=None)),
    Column('default_locale', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('password_hash', String(length=None, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False),  nullable=False),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    meta.create_all()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    meta.drop_all()
