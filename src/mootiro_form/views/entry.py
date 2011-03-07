# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import csv
from cStringIO import StringIO
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form.models import Entry, sas
from mootiro_form.views import BaseView, authenticated
from mootiro_form import _

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

    def _csv_generator(self, entry):
        # TODO: Kommentare!!
        entry = entry.one()
        form = entry.form
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        csvWriter.writerow([self.tr(_('Entry {0}')) \
                           .format (entry.entry_number)])
        # get the data of the fields of the entry e
        fields_data = [[f.label,
                       f.value(entry)]
                       for f in form.fields]
        # create a generator???????????????????????????
        for single_field_data in fields_data:
            csvWriter.writerow(single_field_data)
            row = file.getvalue()
            print(row)
            file.seek(0)
            file.truncate()
            yield row

    @action(name='export', request_method='GET')
    @authenticated
    def create_csv(self):
        # TODO: Comments!!
        entry_id = self.request.matchdict['id']
        entry = sas.query(Entry).filter(Entry.id == entry_id)
        name = self.tr(_('Answers_to_Entry_{0}_{1}.csv')) \
                                             .format(entry.one().entry_number,
                                                     entry.one().created)
        return Response(status='200 OK',
               headerlist=[('Content-Disposition', 'attachment; filename={0}' \
                          .format (name))],
               app_iter=self._csv_generator(entry))


