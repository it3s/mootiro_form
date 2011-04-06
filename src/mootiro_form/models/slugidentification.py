# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models import User, sas
from mootiro_form.utils.text import random_word

from sqlalchemy import Column, Unicode, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

class SlugIdentification(Base):
    '''Represents a userslug to identify the user that wants to reset his
    password.
    *created* is the moment the entry was created.
    *user_id* points to the corresponding user.
    '''
    __tablename__ = "slug_identification"
    id = id_column(__tablename__)
    user_slug = Column(Unicode(10), nullable=False, unique=True)
    created = now_column() # when was this record created

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('slug_identifications',order_by=id,
                        cascade_backrefs='all,delete-orphan'))


    @classmethod
    def create_unique_slug(cls, user):
        # Create the slug to identify the user 
        slug = random_word(10)
        # Ensure that slug is unique
        while sas.query(SlugIdentification) \
             .filter(SlugIdentification.user_slug == slug).first():
                 slug = random_word(10)
        # And return a SlugIdentification instance with the slug
        return SlugIdentification(user_slug=slug, user=user)
