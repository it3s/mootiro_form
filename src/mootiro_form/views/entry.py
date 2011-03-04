# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
from pyramid_handlers import action
from mootiro_form.models import Entry, sas
from mootiro_form.views import BaseView, authenticated

class EntryView(BaseView):
    """The form entry view."""

    @action(name='data', renderer='json', request_method='GET')
    @authenticated
    def entry_data(self):
        entry_id = self.request.matchdict['id']
        entry = sas.query(Entry).get(entry_id)

        if entry.form.user_id == self.request.user.id:
            return entry.fields_data(field_idx="FIELD_LABEL")
        return "No permission"


