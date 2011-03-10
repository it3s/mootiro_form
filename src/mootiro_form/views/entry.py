# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import csv
import deform as d

from cStringIO import StringIO
from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form.utils.form import make_form
from mootiro_form.models import Form, Entry, sas
from mootiro_form.views import BaseView, authenticated
from mootiro_form.schemas.form import create_form_schema
from mootiro_form import _
from mootiro_form.fieldtypes import fields_dict


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
        download from the server.
        '''
        entry_id = self.request.matchdict['id']
        # Assign name of the file dynamically according to form name and
        # creation date
        entry = sas.query(Entry).filter(Entry.id == entry_id).one()
        form = entry.form
        name = self.tr(_('Answers_to_entry_{0}_{1}_of_form_{2}.csv')) \
                                             .format(entry.entry_number,
                                                   unicode(entry.created)[:10],
                                          unicode(form.name).replace(' ', '_'))
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        column_names = [self.tr(_('Entry')), self.tr(_('Creation Date'))] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        # get the data of the fields of one entry e in a list of lists
        fields_data = [entry.entry_number, str(entry.created)[:16]] + \
        [f.value(entry).encode(encoding) for f in form.fields]
        csvWriter.writerow(fields_data)
        entryfile = file.getvalue()
        return Response(status='200 OK',
            headerlist=[(b'Content-Disposition', b'attachment; filename={0}' \
                        .format (name.encode(encoding)))],
            body=entryfile)

    @action(name='view_form', renderer='entry_creation.genshi',
            request_method='GET')
    def view_form(self):
        '''Displays the form so an entry can be created.'''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        if form == None:
            return HTTPNotFound()
        if not form.public:
            return dict(not_published=True)

        form_schema = create_form_schema(form)
        form = make_form(form_schema, i_template='form_mapping_item',
                buttons=['Ok'],
                action=(self.url('entry_form_slug', action='save_entry',
                        slug=form.slug)))
        return dict(form=form.render())

    @action(name='save_entry', renderer='entry_creation.genshi',
            request_method='POST')
    def save_entry(self):
        '''Saves an answer POSTed to the form, and stores a new entry to it.'''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        form_schema = create_form_schema(form)
        dform = d.Form(form_schema, buttons=['Ok'],
                action=(self.url('entry_form_slug', action='save_entry',
                        slug=form.slug)))
        submitted_data = self.request.params.items()

        try:
            form_data = dform.validate(submitted_data)
        except d.ValidationFailure as e:
            return dict(form = e.render())

        entry = Entry()
        entry.created = datetime.utcnow()

        # Get the total number of form entries
        num_entries = sas.query(Entry).filter(Entry.form_id == form.id).count()
        entry.entry_number = num_entries + 1
        form.entries.append(entry)
        sas.add(entry)
        sas.flush()

        # This part the field data is save on DB
        for f in form.fields:
            field_data = fields_dict[f.typ.name](f)
            field_data.save_data(entry, form_data['input-{0}'.format(f.id)])

        return HTTPFound(location=self.url('entry_form_slug', action='thank',
            slug=form.slug))

    @action(name='thank', renderer='entry_creation.genshi')
    def thank(self):
        '''After saving an answer and creating a new entry for the form thank
        the person who filled it.
        '''
        form_slug = self.request.matchdict['slug']
        form = sas.query(Form).filter(Form.slug == form_slug).first()

        tm = form.thanks_message if form.thanks_message \
                else _("We've received you submission. Thank you.")

        return dict(thanks_message=tm)
