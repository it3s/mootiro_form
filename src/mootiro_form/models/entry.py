# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form, sas


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
        if fields == []:
            # Get all text data
            if field_idx == "FIELD_ID":
                fields_data_list =  [{'id': f.id,
                                    'data': f.value(self)}
                                    for f in self.form.fields]
            elif field_idx == "FIELD_LABEL":
                fields_data_list = {'form_title': self.form.name,
                    'entry_number': self.entry_number,
                    'fields': [{'position': f.position + 1,
                                'label': f.label,
                                'data': f.value(self)}
                                for f in self.form.fields]}
        return fields_data_list

    def delete_entry(self):
            sas.delete(self)
            sas.flush()
            return()

    def to_dict(self):
        return {'entry_id': self.id,
                'entry_created': unicode(self.created)[:16],
                'entry_number': self.entry_number,
                'form': self.form.to_dict()}


def pagination(form_id, page, limit):
    offset = page * limit - limit
    return paginated_entries(form_id, offset, limit)


def paginated_entries(form_id, offset, limit):
    paginated_entries = sas.query(Entry).filter(Entry.form_id == form_id) \
                                        .limit(limit).offset(offset).all()
    return paginated_entries

