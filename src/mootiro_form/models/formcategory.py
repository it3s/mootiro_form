# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, UnicodeText, Boolean, Integer, Sequence, \
                       ForeignKey
from sqlalchemy.orm import relationship, backref
from . import Base, id_column, now_column
from .user import User


class FormCategory(Base):
    '''Represents a category into which the user can file forms.'''
    __tablename__ = "form_category"
    id = id_column(__tablename__)
    name = Column(UnicodeText, nullable=False)
    description = Column(UnicodeText, nullable=True)
    position = Column(Integer)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref('categories', order_by=name))

    def __repr__(self):
        return "Category({},{},{},{})".format(self.name,self.description,
                                              self.position, self.user)

    def to_json(self):
        return {'category_id': self.id,
                'category_name': self.name,
                'category_desc': self.description,
                'category_position': self.position,
                'forms': [form.to_json() for form in self.forms]
                }

    def show_all_filter_by_user(self, user):
        ''' This functions gives all the forms and categories a user has, for
        easier editing
        '''
        all_data = list()
        # Now, all the forms which do NOT belong to a category
        # This is mostly a workaround, so the templates can show all the
        # uncategorized forms. 
        all_data.insert(0, {'category_desc': None,
                         'category_id': None,
                         'category_name': 'uncategorized',
                         'category_desc': None,
                         'category_position': None,
                'forms': [form.to_json() for form in sas.query(Form).\
                        filter(Form.user==user).filter(Form.category==None).\
                            all()]
                })
        if user.categories:
            more_data = [category.to_json for category in user.categories]
            all_data.append(more_data)
        
        return all_data

