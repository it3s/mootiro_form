# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from datetime import datetime
import json
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from mootiro_form import _
from mootiro_form.models import Entry, Form, sas
from mootiro_form.views import BaseView, authenticated
from mootiro_form.fieldtypes import all_fieldtypes

class EntryView(BaseView):
    """The form entry view."""

    @action(name='data', renderer='json', request_method='GET')
    @authenticated
    def entry_data(self):
        entry_id = self.request.matchdict['id']
        entry = sas.query(Entry).get(entry_id)

        return entry.fields_data(field_idx="FIELD_LABEL")

