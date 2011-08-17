# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import os.path

import csv
import deform as d

from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form.models import sas
from mootiro_form.models.file_data import FileData
from mootiro_form.views import BaseView, authenticated
from mootiro_form.views.entry import EntryView
from mootiro_form import _


class FileView(BaseView):
    """The form entry view."""

    @action(name='image_preview', request_method='GET')
    def file_preview(self):
        from mootiro_form.fieldtypes.image import tmpstore

        uid = self.request.matchdict['id']
        data = tmpstore.get(uid)
        if not data:
            return HTTPNotFound()

        mimetype = data['mimetype']
        if not mimetype.startswith('image/'):
            return HTTPNotFound()
        try:
            return Response(content_type=mimetype,
                            app_iter=open(data['path'], 'rb'))
        except IOError:
            return HTTPNotFound()

    @action(name='view', request_method='GET')
    @authenticated
    def view(self):
        entry_id = self.request.matchdict['id']
        field_id = self.request.matchdict['field']
        entryview = EntryView(self.request)
        entry, form = entryview._get_entry_and_form_if_belongs_to_user(
            entry_id=entry_id)
        if entry and form:
            data = sas.query(FileData) \
                    .filter(FileData.entry_id == entry_id) \
                    .filter(FileData.field_id == field_id).first()
            path = data.path
            if not path or not os.path.isfile(path):
                return HTTPNotFound()
            try:
                response = Response(content_type=data.mimetype,
                                    app_iter=open(path, 'rb'))
            except:
                return HTTPNotFound()
            finally:
                return response
        return _("Access denied")

    @action(name='thumbnail', request_method='GET')
    @authenticated
    def thumbnail(self):
        entry_id = self.request.matchdict['id']
        field_id = self.request.matchdict['field']
        entryview = EntryView(self.request)
        entry, form = entryview._get_entry_and_form_if_belongs_to_user(
            entry_id=entry_id)
        if entry and form:
            data = sas.query(FileData) \
                    .filter(FileData.entry_id == entry_id) \
                    .filter(FileData.field_id == field_id).first()
            path = data.thumbnail_path
            if not path or not os.path.isfile(path):
                return HTTPNotFound()
            try:
                response = Response(content_type=data.mimetype,
                                    app_iter=open(path, 'rb'))
            except:
                return HTTPNotFound()
            finally:
                return response
        return _("Access denied")

