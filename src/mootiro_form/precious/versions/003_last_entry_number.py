from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()
Base = declarative_base(metadata=meta)

def upgrade(migrate_engine):
    # Add column last_entry_number to form table to have a sequential counter
    # of the number of the entries
    meta.bind = migrate_engine
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
    c = Column('last_entry_number', Integer(), default=0)
    c.create(t, populate_default=True)

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
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
        last_entry_number = Column(Integer, default=0)
    t = Form.__table__
    t.c.last_entry_number.drop()

