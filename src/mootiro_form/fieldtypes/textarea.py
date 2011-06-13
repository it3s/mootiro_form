# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default
import deform as d
from mootiro_form import _
from mootiro_form.fieldtypes.text import TextBase


class TextAreaField(TextBase):
    name = _('Multiline text')
    brief = _("multiline text")
    defaultValue = dict(defaul='', required=False)

    def get_widget(self):
        f = self.field
        return d.widget.TextAreaWidget(template='form_textarea',
            style='width:{}px; height: {}px;'.format(f.get_option('width'),
            f.get_option('height')))

    _special_options = 'defaul enableLength minLength maxLength enableWords ' \
                 'minWords maxWords height width'.split()
