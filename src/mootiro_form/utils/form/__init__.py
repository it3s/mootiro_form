# -*- coding: utf-8 -*-

import deform as d

def make_form(form_schema, f_template='form', i_template='mapping_item', *args, **kwargs):
    form = d.Form(form_schema, *args, **kwargs)
    class F(d.widget.FormWidget):
        template = f_template
        item_template = i_template
    form.set_widgets({'':F()})
    return form

