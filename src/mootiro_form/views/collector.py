# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from pyramid.response import Response
from mootiro_form import _
from mootiro_form.models.collector import PublicLinkCollector, sas
from mootiro_form.views import BaseView, authenticated, safe_json_dumps
from mootiro_form.views.form import FormView


class CollectorView(BaseView):
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

        # TODO Validate `posted` with colander:
        '''
        try:
            posted = some_schema.deserialize(posted)
        except c.Invalid as e:
            return e.asdict()
        '''

        # Validation passes, so create or update the model.
        if id == 'new':
            collector = PublicLinkCollector(form=form)
            sas.add(collector)
        else:
            collector = sas.query(PublicLinkCollector).get(id)

        # Copy the data
        print(posted)
        # collector.blah = posted['blorgh']

        sas.flush()
        return dict(id=collector.id,)
