# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from sqlalchemy import Column, Unicode, UnicodeText, Integer, ForeignKey, desc
from sqlalchemy.orm import relationship, backref

from mootiro_form.models import Base, id_column, now_column
from mootiro_form.models.form import Form, sas

class FileUploadTempStore(Base):

    __tablename__ = "file_upload_temp_store"
    id = id_column(__tablename__)
    created = now_column()

    uid = Column(Unicode(10), nullable=False)
    mimetype = Column(Unicode(255)) #http://tools.ietf.org/html/rfc4288#section-4.2
    filename = Column(UnicodeText)
    size = Column(Integer)
    path = Column(UnicodeText)
    thumbnail_path = Column(UnicodeText)

    def to_dict(self):
        d = {k: getattr(self, k) for k in ('created', 'uid',
            'mimetype', 'filename', 'size', 'path', 'thumbnail_path')}
        return d

