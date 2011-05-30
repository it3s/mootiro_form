from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from migrate import *

meta = MetaData()
Base = declarative_base(metadata=meta)

def upgrade(migrate_engine):
    meta.bind = migrate_engine

    class WebsiteCodeCollector(Base):
        __tablename__ = 'website_code_collector'
        __mapper_args__ = {'polymorphic_identity': 'website_code'}
        id = Column(Integer, ForeignKey('collector.id'), primary_key=True)
        embed_frame_height = Column(Integer)

    t = WebsiteCodeCollector.__table__
    c = Column('invitation_message', UnicodeText())
    c.create(t, populate_default=True)


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    class WebsiteCodeCollector(Base):
        __tablename__ = 'website_code_collector'
        __mapper_args__ = {'polymorphic_identity': 'website_code'}
        id = Column(Integer, ForeignKey('collector.id'), primary_key=True)
        invitation_message = Column(UnicodeText)
        embed_frame_height = Column(Integer)

    t = WebsiteCodeCollector.__table__
    t.c.invitation_message.drop()
