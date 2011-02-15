# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import User

from sqlalchemy import Column, Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

class ForgottenPassword(Base):
    '''Represents a userslug to identify the user that wants to reset his
    password.
    *created* is the moment the entry was created.
    *user_id* points to the corresponding user.
    '''
    __tablename__ = "forgotten_password"
    id = id_column(__tablename__)
    user_slug = Column(Unicode(10), nullable=False, unique=True)
    created = now_column() # when was this record created

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('forgotten_passwords', order_by=id))
