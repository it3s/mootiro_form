# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c

from datetime import datetime

from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from pyramid.response import Response
from pyramid.renderers import render
from mootiro_form import _
from mootiro_form.models import sas
from mootiro_form.models.form import Form
from mootiro_form.models.collector import Collector, PublicLinkCollector, \
                                          WebsiteCodeCollector
from mootiro_form.schemas.collector import public_link_schema, \
                                           website_code_schema
from mootiro_form.views import BaseView, authenticated, safe_json_dumps
from mootiro_form.views.form import FormView


class CollectorView(BaseView):
    @action(renderer='form_collectors.genshi')
    @authenticated
    def collectors(self):
        '''Displays all collectors of a form.'''
        # TODO Don't convert to int here, use the regex in Pyramid routes
        form_id = int(self.request.matchdict['id'])
        form = FormView(self.request)._get_form_if_belongs_to_user(form_id=form_id)
        collectors = [c.to_dict() for c in form.collectors]
        collectors_json = safe_json_dumps(collectors)
        return dict(form=form, collectors_json=collectors_json,
            pagetitle=_('Collectors for {0}').format(form.name))

    @action(renderer='json', request_method='POST')
    @authenticated
    def save_public_link(self):
        '''Responds to the AJAX request and saves a collector.'''
        request = self.request
        posted = request.POST
        id = request.matchdict['id']
        form_id = request.matchdict['form_id']
        form = FormView(request)._get_form_if_belongs_to_user(form_id=form_id)
        if not form:
            return dict(error=_("Error finding form"))

        # Validate `posted` with colander:
        try:
            posted = public_link_schema.deserialize(posted)
        except c.Invalid as e:
            return e.asdict()

        # Validation passes, so create or update the model.
        if id == 'new':
            collector = PublicLinkCollector(form=form)
            sas.add(collector)
        else:
            collector = self._get_collector_if_belongs_to_user(id)
        # Copy the data
        self._parse_start_and_end_date(posted)
        for k, v in posted.items():
            setattr(collector, k, v)
        sas.flush()
        return collector.to_dict()

    @action(renderer='json', request_method='POST')
    @authenticated
    def save_website_code(self):
        '''Responds to the AJAX request and saves a collector.'''
        request = self.request
        posted = request.POST
        id = request.matchdict['id']
        form_id = request.matchdict['form_id']
        form = FormView(request)._get_form_if_belongs_to_user(form_id=form_id)
        if not form:
            return dict(error=_("Error finding form"))

        # Validate `posted` with colander:
        try:
            posted = website_code_schema.deserialize(posted)
        except c.Invalid as e:
            return e.asdict()

        # Validation passes, so create or update the model.
        if id == 'new':
            collector = WebsiteCodeCollector(form=form)
            sas.add(collector)
        else:
            collector = self._get_collector_if_belongs_to_user(id)
        # Copy the data
        self._parse_start_and_end_date(posted)
        for k, v in posted.items():
            setattr(collector, k, v)
        sas.flush()
        return collector.to_dict()

    @action(name='popup_survey')
    @action(name='popup_invitation')
    def popup (self):
        '''Returns a file with js code for opening the pop-up.'''
        collector, form = self._get_collector_and_form()
        action = self.request.matchdict['action']
        tpl_string = render('collector_popup.mako',
                        dict(collector=collector, action=action),
                        request=self.request)
        return Response(status='200 OK',
               headerlist=[(b'Content-Type', b'text/javascript')],
               body=tpl_string)

    @action(name='invite', renderer='collector.genshi')
    def invite(self):
        collector, form = self._get_collector_and_form()
        action = self.request.matchdict['action']
        return dict(collector=collector, action=action)

    def _get_collector_and_form(self, slug=None):
        if not slug:
            slug = self.request.matchdict['slug']
        return sas.query(Collector, Form).join(Form) \
            .filter(Collector.slug == slug).one()

    def _get_collector_if_belongs_to_user(self, collector_id=None):
        if not collector_id:
            collector_id = self.request.matchdict['id']
        return sas.query(Collector).join(Form) \
            .filter(Collector.id == collector_id) \
            .filter(Form.user == self.request.user).first()


    def _parse_start_and_end_date(self, posted):
        start_date = posted['start_date']
        end_date = posted['end_date']
        if start_date:
            posted['start_date'] = datetime.strptime(start_date,
                                                "%Y-%m-%d %H:%M")
        else:
            posted['start_date'] = None
        if end_date:
            posted['end_date'] = datetime.strptime(end_date,
                                              "%Y-%m-%d %H:%M")
        else:
            posted['end_date'] = None
        return posted


    @action(renderer='json')
    @authenticated
    def as_json(self):
        '''Retrieve collector information as a json object'''
        return self._get_collector_if_belongs_to_user().to_dict()

    @action(renderer='json')
    @authenticated
    def delete(self):
        collector = self._get_collector_if_belongs_to_user()
        if collector:
            sas.delete(collector)
            sas.flush()
            error = ''
        else:
            error = _("This collector doesn't exist!")
        return {'errors': error}

