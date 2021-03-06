# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Integer, ForeignKey, Boolean, desc
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form, sas
from mootiro_form.models.collector import Collector


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
    new = Column(Boolean, default=True)

    form_id = Column(Integer, ForeignKey('form.id'), index=True)
    form = relationship(Form, backref=backref('entries', order_by=(desc(created)),
                                              cascade='all'))

    collector_id = Column(Integer, ForeignKey('collector.id'), index=True)
    collector = relationship(Collector,
        backref=backref('entries', order_by=id))

    def fields_data(self, field_idx="FIELD_ID", fields=[], request=None):
        url = request.application_url if request else ''
        if fields == []:
            # Get all text data
            if field_idx == "FIELD_ID":
                fields_data_list =  [{'id': f.id,
                                    'data': f.value(self).format(url=url)}
                                    for f in self.form.fields]
            elif field_idx == "FIELD_LABEL":
                fields_data_list = {'form_title': self.form.name,
                    'entry_id': self.id,
                    'entry_number': self.entry_number,
                    'fields': [{'position': f.position + 1,
                                'label': f.label,
                                'data': f.value(self).format(url=url),
                                'type': f.typ.name}
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
                'entry_new': self.new}


def pagination(form_id, page=1, limit=10):
    offset = page * limit - limit
    return paginated_entries(form_id, offset, limit)


def paginated_entries(form_id, offset, limit):
    paginated_entries = sas.query(Entry).filter(Entry.form_id == form_id) \
                                        .order_by(desc(Entry.created)) \
                                        .limit(limit).offset(offset).all()
    return paginated_entries

