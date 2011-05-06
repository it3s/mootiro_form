# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form import _
from mootiro_form.models import get_length, sas
from mootiro_form.models.form import Form
from mootiro_form.models.collector import PublicLinkCollector, Collector
from mootiro_form.views import BaseView, authenticated, safe_json_dumps
from mootiro_form.views.form import FormView


class PublicLinkSchema(c.MappingSchema):
    name = c.SchemaNode(c.Str(),
           validator=c.Length(max=get_length(PublicLinkCollector, 'name')))
    on_completion = c.SchemaNode(c.Str(),
                validator=c.OneOf(Collector.ON_COMPLETION_VALUES))
    thanks_url = c.SchemaNode(c.Str(), missing='',
           validator=c.Length(max=get_length(Collector, 'thanks_url')))
    thanks_message = c.SchemaNode(c.Str(), missing='')

    limit_by_date = c.SchemaNode(c.Boolean(), missing=False)
    start_date = c.SchemaNode(c.DateTime(), missing=None)
    end_date = c.SchemaNode(c.DateTime(), missing=None)
    message_after_end = c.SchemaNode(c.Str(), missing='')
    message_before_start = c.SchemaNode(c.Str(), missing='')


public_link_schema = PublicLinkSchema()


class CollectorView(BaseView):
    @action(renderer='form_collectors.genshi')
    @authenticated
    def collectors(self):
        '''Displays all collectors of a form.'''
        # TODO Don't convert to int here, use the regex in Pyramid routes
        form_id = int(self.request.matchdict['id'])
        form = FormView(self.request)._get_form_if_belongs_to_user(form_id)
        collectors = [c.to_dict() for c in form.collectors]
        collectors_json = safe_json_dumps(collectors)
        return dict(form=form, collectors_json=collectors_json,
            pagetitle='Collectors for {0}'.format(form.name))

    @action(renderer='json', request_method='POST')
    @authenticated
    def save_public_link(self):
        '''Responds to the AJAX request and saves a collector.'''
        request = self.request
        posted = request.POST
        id = request.matchdict['id']
        form_id = request.matchdict['form_id']
        form = FormView(request)._get_form_if_belongs_to_user(form_id)
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
            # collector = sas.query(PublicLinkCollector).get(id)
            collector = self._get_collector_if_belongs_to_user(id)
        assert isinstance(collector, PublicLinkCollector)
        # Copy the data
        for k, v in posted.items():
            setattr(collector, k, v)

        sas.flush()
        return collector.to_dict()

    def _get_collector_if_belongs_to_user(self, collector_id=None):
        if not collector_id:
            collector_id = self.request.matchdict['id']
        return sas.query(Collector).join(Form) \
            .filter(Collector.id == collector_id) \
            .filter(Form.user == self.request.user).first()

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
