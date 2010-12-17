from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, ForeignKey

from formcreator.models import Base

class Field(Base):
    __tablename__ = "field"
    id = Column(Integer, Sequence('field_id_seq'), primary_key=True)
    form_id = Column(Integer, ForeignKey('form.id'))
    label = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    title = Column(UnicodeText, nullable=False)
    help_text = Column(UnicodeText, nullable=False)
    position = Column(Integer)
    required = Column(Boolean)
