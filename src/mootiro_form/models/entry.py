# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form


class Entry(Base):
    '''Represents a form entry.
    *created* is the moment the entry was created
    *form_id* points to the corresponding form.
    *entry_number* is the number of an entry.
    '''
    __tablename__ = "entry"
    id = id_column(__tablename__)
    created = now_column()  # when was this record created
    entry_number = Column(Integer)

    form_id = Column(Integer, ForeignKey('form.id'))
    form = relationship(Form, backref=backref('entries', order_by=id))

    def fields_data(self, field_idx="FIELD_ID", fields=[]):
        field_data_dict = {}
        if fields == []:
            # Get all text data
            if field_idx == "FIELD_ID":
                field_data_dict =  [{'id': d.field.id,
                                    'data': d.value}
                                    for d in self.text_data]
            elif field_idx == "FIELD_LABEL":
                field_data_dict = [{'label': d.field.label,
                                    'data': d.value}
                                    for d in self.text_data]

        return field_data_dict

