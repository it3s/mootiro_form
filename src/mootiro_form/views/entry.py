# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import csv
import deform as d

from cStringIO import StringIO
from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid_handlers import action
from pyramid.response import Response
from pyramid.renderers import render
from mootiro_form.utils.form import make_form
from mootiro_form.models import Collector, Form, Entry, sas
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

        # User validation
        if entry.form.user_id == self.request.user.id:
            return entry.fields_data(field_idx="FIELD_LABEL")
        return _("No permission")

    @action(name='delete', renderer='json', request_method='POST')
    @authenticated
    def delete_entry(self):
        entry_id = self.request.matchdict['id']
        entry = sas.query(Entry).get(entry_id)

        # User validation
        if entry.form.user_id == self.request.user.id:
            entry.delete_entry()
            return dict(errors=None,entry=entry_id)
        return _("You're not allowed to delete this entry")

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
        name = self.tr(_('Entry_{0}_{1}_of_form_{2}.csv')) \
                                 .format(entry.entry_number,
                            unicode(entry.created)[:10],
                            unicode(form.name[:200]).replace(' ', '_'))
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        column_names = [self.tr(_('Entry')).encode(encoding),
                        self.tr(_('Submissions (Date, Time)')) \
                                  .encode(encoding)] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        # get the data of the fields of one entry e in a list of lists
        fields_data = [entry.entry_number, str(entry.created)[:16]] + \
        [f.value(entry).encode(encoding) for f in form.fields]
        csvWriter.writerow(fields_data)
        entryfile = file.getvalue()
        return Response(status='200 OK',
            headerlist=[(b'Content-Type', b'text/comma-separated-values'),
                        (b'Content-Disposition', b'attachment; filename={0}' \
                        .format (name.encode(encoding)))],
            body=entryfile)

    def _get_collector_and_form(self, slug=None):
        if not slug:
            slug = self.request.matchdict['slug']
        return sas.query(Collector, Form).join(Form) \
            .filter(Collector.slug == slug).one()

    def _get_collector(self, slug=None):
        if not slug:
            slug = self.request.matchdict['slug']
        return sas.query(Collector).filter(Collector.slug == slug).one()

    def _get_schema_and_form(self, form, slug=None):
        if not slug:
            slug = self.request.matchdict['slug']
        form_schema = create_form_schema(form)
        entry_form = make_form(form_schema, i_template='form_mapping_item',
            buttons=[form.submit_label if form.submit_label else _('Submit')],
            action=(self.url('entry_form_slug', action='save_entry',
                    slug=slug)))
        return form_schema, entry_form

    @action(name='view_form', renderer='entry_creation.genshi',
            request_method='GET')
    def view_form(self):
        '''Displays the form if published and accessible so an
        entry can be created. Else renders a corresponding message.
        '''
        collector, form = self._get_collector_and_form()
        if collector is None:
            return HTTPNotFound()
        form_schema, entry_form = self._get_schema_and_form(form)
        return dict(collector=collector, entry_form=entry_form.render(),
                    form=form)

    @action(name='template')
    def css_template(self):
        '''Returns a file with css rules for the entry creation form.'''
        collector, form = self._get_collector_and_form()
        fonts, colors = form.template.css_template_dicts()
        #render the template as string to return it in the body of the response
        tpl_string = render('entry_creation_template.mako',
                             dict(f=fonts, c=colors), request=self.request)
        return Response(status='200 OK',
               headerlist=[(b'Content-Type', b'text/css')],
               body=tpl_string)

    @action(name='save_entry', renderer='entry_creation.genshi',
            request_method='POST')
    def save_entry(self):
        '''Saves an answer POSTed to the form, and stores a new entry to it.'''
        collector, form = self._get_collector_and_form()
        if collector is None:
            return HTTPNotFound()
        form_schema, entry_form = self._get_schema_and_form(form)
        form_data = self.request.params.items()
        try:
            form_data = entry_form.validate(form_data)
        except d.ValidationFailure as e:
            return dict(collector=collector, entry_form=e.render(), form=form)
        entry = Entry()
        # Get the last increment of the entry number and update entry and form
        new_entry_number = form.last_entry_number + 1
        form.last_entry_number = new_entry_number
        entry.entry_number = new_entry_number
        entry.form = form  # form.entries.append(entry)
        entry.collector = collector
        sas.add(entry)
        sas.flush()
        for f in form.fields:
            field = fields_dict[f.typ.name](f)
            field.save_data(entry, form_data['input-{}'.format(f.id)])
        if collector.on_completion=='url' and collector.thanks_url:
            return HTTPFound(location=collector.thanks_url)
        else:
            return HTTPFound(location=self.url('entry_form_slug',
                action='thank', slug=collector.slug))

    @action(name='thank', renderer='entry_creation.genshi')
    def thank(self):
        '''After creating a new entry for the form, thank the user.'''
        collector, form = self._get_collector_and_form()
        tm = collector.thanks_message
        return dict(thanks_message=tm, collector=collector, form=form)
