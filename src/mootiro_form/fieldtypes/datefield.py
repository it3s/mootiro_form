# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d
from datetime import datetime

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.date_data import DateData
from mootiro_form.models.field_option import FieldOption


class DateFormats(object):
    formats = []

    def add(self, py, js, fv=None):
        if fv:
            self.formats.append({'py': py, 'js': js, 'format_value': fv})
        else:
            self.formats.append({'py': py, 'js': js})

df = DateFormats()
# 30/9/99
df.add('%d/%m/%y','d/m/y', lambda date: '{0}/{1}/{2}'. \
                    format(date.day, date.month, str(date.year)[2:]))
# 30/09/99
df.add('%d/%m/%y', 'd/mm/y')
# 30/9/1999
df.add('%d/%m/%Y', 'd/m/yy', lambda date: '{0}/{1}/{2}'. \
        format(date.day, date.month, date.year))
# 30/09/1999
df.add('%d/%m/%Y', 'd/mm/yy')
# 9/30/99
df.add('%m/%d/%y','d/m/y', lambda date: '{0}/{1}/{2}'. \
                    format(date.month, date.day, str(date.year)[2:]))
# 09/30/99
df.add('%m/%d/%y', 'mm/dd/y')
# 9/30/1999
df.add('%m/%d/%Y', 'm/dd/yy', lambda date: '{0}/{1}/{2}'. \
                format(str(date.month)[2:], date.day, date.year))
# 09/30/1999
df.add('%m/%d/%Y', 'mm/dd/yy')
# 99-09-30
df.add('%y-%m-%d', 'y-mm-d')
# 1999-09-30
df.add('%Y-%m-%d', 'yy-mm-d')
# 30.9.99
df.add('%d.%m.%y', 'dd.m.y', lambda date: '{0}.{1}.{2}'. \
                format(date.day, str(date.month), date.year))
# 30.09.99
df.add('%d.%m.%y', 'dd.m.y')
# 30.9.1999
df.add('%d.%m.%Y', 'dd.m.yy', lambda date: '{0}.{1}.{2}'. \
                format(date.day, str(date.month), date.year))
# 30.09.1999
df.add('%d.%m.%Y', 'dd.mm.yy')
# Sep 1, 99
df.add("%b %d, %y" ,'M d, y', lambda date: \
        date.strftime('%b {0}, %y').format(str(date.day)))
# Sep 01, 99
df.add("%b %d, %y" ,'M d, y')
# Sep 1, 1999
df.add("%b %d, %Y" ,'M d, yy', lambda date: \
        date.strftime('%b {0}, %y').format(str(date.day)))
# Sep 01, 1999
df.add("%b %d, %Y" ,'M d, yy')
# 01. Sep. 99
df.add("%d. %b. %y" ,'d. M. y')
# 01. Sep. 1999
df.add("%d. %b. %Y" ,'d. M. yy')
# September 30, 1999
df.add("%B %d, %Y" ,'MM d, yy')
# 30. September 1999
df.add("%d. %B %Y" ,'d. MM yy')

class DateField(FieldType):
    name = _('Date input')
    brief = _("Select a simple date")

    defaultValue = dict(defaul='',
                        input_date_format='%Y-%m-%d',
                        export_date_format='%Y-%m-%d',
                        required=False)

    def initJson(self):
        return dict(date_formats=map(lambda f: f['js'], df.formats))

    def value(self, entry):
        date_format = self.field.get_option('export_date_format')
        data = sas.query(DateData) \
                .filter(DateData.field_id == self.field.id) \
                .filter(DateData.entry_id == entry.id).first()
        return data.value.strftime(date_format) if data else ''

    def parseDate(self, data):
        pass

    def formatDate(self, data):
        pass

    def get_schema_node(self):
        widget = d.widget.DateInputWidget(template='form_date')
        date_default = self.field.get_option('defaul')
        if date_default != '':
            default = {'default':datetime.strptime(date_default, \
                            self.field.get_option('input_date_format'))}
        else:
            default = {}

        if self.field.required:
            sn = c.SchemaNode(c.Date(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                description=self.field.description, widget=widget,
                **default
                )
        else:
            sn = c.SchemaNode(c.Date(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                missing=c.null,
                description=self.field.description, widget=widget,
                **default
                )

        return sn

    def save_data(self, entry, value):
        if value != c.null:
            self.data = DateData()
            self.data.field_id = self.field.id
            self.data.entry_id = entry.id
            self.data.value = value
            sas.add(self.data)

    def save_options(self, options):
        '''Called by the form editor view in order to persist field properties.
        '''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        self.save_option('input_date_format', options['input_date_format'])
        self.save_option('export_date_format', options['export_date_format'])
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])

    def save_option(self, option, value):
        '''Updates or creates the value of a field option.'''
        opt = sas.query(FieldOption).filter(FieldOption.option == option) \
                       .filter(FieldOption.field_id == self.field.id).first()
        if opt:
            opt.value = value
        else:
            new_option = FieldOption(option, value)
            self.field.options.append(new_option)

    def schema_options(self):
        pass

    def to_dict(self):
        d = dict(
            type=self.field.typ.name,
            label=self.field.label,
            field_id=self.field.id,
            required=self.field.required,
            input_date_format=self.field.get_option('input_date_format'),
            export_date_format=self.field.get_option('export_date_format'),
            description=self.field.description,
            defaul=self.field.get_option('defaul'),
        )
        # Add to the dict all the options of this field
        d.update({o.option: o.value for o in self.field.options})
        return d
