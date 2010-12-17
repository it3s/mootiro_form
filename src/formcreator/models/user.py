from sqlalchemy import Column, Unicode, Integer, Sequence

from formcreator.models import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(Unicode, nullable=False, unique=True)
    name = Column(Unicode)
    password_hash = Column(Unicode)
    email = Column(Unicode)

