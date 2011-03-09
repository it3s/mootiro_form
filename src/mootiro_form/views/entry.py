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

    @action(name='export', request_method='GET')
    @authenticated
    def create_csv(self, encoding='utf-8'):
        '''Exports one entry to a form as csv file and initializes
        download from the server'''
        entry_id = self.request.matchdict['id']
        # Assign name of the file dynamically according to form name and
        # creation date
        entry = sas.query(Entry).filter(Entry.id == entry_id).one()
        form = entry.form
        name = self.tr(_('Answers_to_entry_{0}_{1}_of_form_{2}.csv')) \
                                             .format(entry.entry_number,
                                                   unicode(entry.created)[:10],
                                                   form.name)
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        column_names = [self.tr(_('Entry'))] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        # get the data of the fields of one entry e in a list of lists
        fields_data = [entry.entry_number] + \
        [f.value(entry).encode(encoding) for f in form.fields]
        csvWriter.writerow(fields_data)
        entryfile = file.getvalue()
        return Response(status='200 OK',
               headerlist=[(b'Content-Disposition', b'attachment; filename={0}' \
                          .format (name.encode(encoding)))],
               body=entryfile)


