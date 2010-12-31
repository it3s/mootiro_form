# -*- coding: utf-8 -*-
from __future__ import unicode_literals # unicode by default

from hashlib import sha1
from sqlalchemy import Column, Unicode, Integer, Sequence
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from formcreator.models import Base, id_column, now_column

# Auth models: User, Group, Permission
# ====================================

class User(Base):
    '''Represents a user of the application: someone who creates forms.
    *nickname* is a short name used for displaying in small spaces.
    *real_name* is supposed to be the real thing ;)
    *email* is what we really use for login.
    *password_hash* is used for password verification; we don't store the
    actual password for security reasons.
    *password* is a property so you can just set it and forget about the hash.
    This can also store phones and one address.
    '''
    __tablename__ = "user"
    id = id_column(__tablename__)
    created = now_column() # when was this user created
    changed = now_column() # when did the user last update their data
    nickname = Column(Unicode(32), nullable=False, unique=True)
    real_name = Column(Unicode(240))
    email = Column(Unicode(255), nullable=False, unique=True)
    organization = Column(Unicode(160), default='')
    phones = Column(Unicode(160), default='') # one per line
    newsletter = Column(Boolean, default=False) # wishes to receive news?
    # Address:
    street   = Column(Unicode(160), default='')
    district = Column(Unicode(80), default='')
    city     = Column(Unicode(80), default='')
    province = Column(Unicode(60), default='')
    country  = Column(Unicode(40), default='')
    zipcode  = Column(Unicode(20), default='')
    
    password_hash = Column(Unicode(40), nullable=False)
    
    @classmethod
    def calc_hash(cls, password):
        '''Creates the password hash that is actually saved to the database.
        The returned hash is a unicode object containing a
        40 character long hexadecimal number.
        For this to work, a *salt* string must have been added to this class
        during configuration. (Yeah, monkeypatching.)
        This way the salt will be different for each
        installation of FormCreator (which is an open source app).
        '''
        return unicode(sha1(cls.salt + password).hexdigest())
    
    @property
    def password(self):
        '''Transient property, does not get persisted.'''
        return self.__dict__.get('_password') # may return None
    @password.setter
    def password(self, password):
        self._password = password
        self.password_hash = User.calc_hash(password)
    
    def __repr__(self):
        return '[ {0}: {1} <{2}> ]'.format(self.id, self.nickname, self.email)
    
    def __unicode__(self):
        return self.nickname or ''


def authenticate(email, password):
    password_hash = User.calc_hash(password)
    return sas.query(User).filter(User.email==email) \
        .filter(User.password_hash == password_hash).one()


''' TODO: We are probably not going to need
traditional User-Group-Permission security; instead:
Possibilidade de criação de grupos de usuários por um usuário, convidando outro usuário a participar mediante confirmação, para o efeito de criar formulários a serem respondidos por certos pesquisadores sem necessidade de escolhê-los todas as vezes.

class Group(Base):
    __tablename__ = 'group'
    id = id_column(__tablename__)
    name = Column(Unicode(32), unique=True, nullable=False)
    description = Column(Unicode(255), nullable=False)
    created = now_column()
'''
