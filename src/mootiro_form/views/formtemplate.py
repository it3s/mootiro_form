# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

from pyramid_handlers import action
from mootiro_form.models import Form, sas, FormTemplate, FormTemplateFont, \
                                FormTemplateColor
from mootiro_form.views import BaseView, authenticated


class FormTemplateView(BaseView):
    """Views for form templates"""

    @action(name='system_template', renderer='json')
    @authenticated
    def get_system_template(self):
        st_id = self.request.matchdict['id']
        template = sas.query(FormTemplate) \
            .filter(FormTemplate.system_template_id == st_id).one()

        return dict(bg=template.colors[0].hexcode)