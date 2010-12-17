from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, ForeignKey

from formcreator.models import Base

class FormCategory(Base):
    __tablename__ = "form_category"
    id = Column(Integer, Sequence('form_category_id_seq'), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    position = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
