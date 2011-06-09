# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import colander as c
import deform as d
from datetime import datetime
import json

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.date_data import DateData


class DateFormats(object):
    formats = []

    def add(self, desc, py, js, fv=None):
        if fv:
            self.formats.append({'desc': desc, 'py': py, 'js': js,
                'format_value': fv})
        else:
            self.formats.append({'desc': desc, 'py': py, 'js': js})


df = DateFormats()
# 30/9/99
df.add('30/9/99', '%d/%m/%y','d/m/y', lambda date: '{0}/{1}/{2}'. \
                    format(date.day, date.month, str(date.year)[2:]))
# 30/09/99
df.add('30/09/99', '%d/%m/%y', 'dd/mm/y')
# 30/9/1999
df.add('30/9/1999', '%d/%m/%Y', 'd/m/yy', lambda date: '{0}/{1}/{2}'. \
        format(date.day, date.month, date.year))
# 30/09/1999
df.add('30/09/1999', '%d/%m/%Y', 'dd/mm/yy')
# 9/30/99
df.add('9/30/99', '%m/%d/%y','m/d/y', lambda date: '{0}/{1}/{2}'. \
                    format(date.month, date.day, str(date.year)[2:]))
# 09/30/99
df.add('09/30/99', '%m/%d/%y', 'mm/dd/y')
# 9/30/1999
df.add('9/30/1999', '%m/%d/%Y', 'm/d/yy', lambda date: '{0}/{1}/{2}'. \
                format(str(date.month)[2:], date.day, date.year))
# 09/30/1999
df.add('09/30/1999', '%m/%d/%Y', 'mm/dd/yy')
# 99-09-30
df.add('99-09-30', '%y-%m-%d', 'y-mm-dd')
# 1999-09-30
df.add('1999-09-30', '%Y-%m-%d', 'yy-mm-dd')
# 30.9.99
df.add('30.9.99', '%d.%m.%y', 'd.m.y', lambda date: '{0}.{1}.{2}'. \
                format(date.day, str(date.month), date.year))
# 30.09.99
df.add('30.09.99', '%d.%m.%y', 'dd.mm.y')
# 30.9.1999
df.add('30.9.1999', '%d.%m.%Y', 'd.m.yy', lambda date: '{0}.{1}.{2}'. \
                format(date.day, str(date.month), date.year))
# 30.09.1999
df.add('30.09.1999', '%d.%m.%Y', 'dd.mm.yy')
# Sep 1, 99
df.add('Sep 1, 99', "%b %d, %y" ,'M d, y', lambda date: \
        date.strftime('%b {0}, %y').format(str(date.day)))
# Sep 01, 99
df.add('Sep 01, 99', "%b %d, %y" ,'M dd, y')
# Sep 1, 1999
df.add('Sep 1, 1999', "%b %d, %Y" ,'M d, yy', lambda date: \
        date.strftime('%b {0}, %y').format(str(date.day)))
# Sep 01, 1999
df.add('Sep 01, 1999', "%b %d, %Y" ,'M dd, yy')
# 01. Sep. 99
df.add('01. Sep. 99', "%d. %b. %y" ,'dd. M. y')
# 01. Sep. 1999
df.add('01. Sep. 1999', "%d. %b. %Y" ,'dd. M. yy')
# September 1, 1999
df.add('September 1, 1999', "%B %d, %Y" ,'MM d, yy')
# 1. September 1999
df.add('1. September 1999', "%d. %B %Y" ,'d. MM yy')


class DateField(FieldType):
    name = _('Date input')
    brief = _("date field")

    defaultValue = dict(defaul='',
                        input_date_format='%Y-%m-%d',
                        export_date_format='%Y-%m-%d',
                        month_selector=False,
                        year_selector=False,
                        show_week=False,
                        required=False)

    def initJson(self):
        return dict(date_formats=map(lambda f:
            {'desc': f['desc'], 'js': f['js']}, df.formats))

    def value(self, entry):
        date_format = df.formats[int(self.field.get_option
            ('export_date_format'))]['py']
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
        month_selector = True if self.field.get_option('month_selector') == 'true' else False
        year_selector = True if self.field.get_option('year_selector') == 'true' else False
        show_week = True if self.field.get_option('show_week') == 'true' else False

        calendar_config= dict(changeMonth=month_selector,
                              changeYear=year_selector,
                              showWeek=show_week,
                              dateFormat=df.formats[int(self.field.get_option \
                                    ('input_date_format'))]['js'])

        calendar_config_json = json.dumps(calendar_config)

        if date_default != '':
            default = {'default':date_default}
        else:
            default = {}

        def date_validation(node, val):
            try:
                date = datetime.strptime(val,
                    df.formats[int(self.field.get_option \
                        ('input_date_format'))]['py'])
            except ValueError:
                raise c.Invalid(node, _("Invalid date format"))

        if self.field.required:
            sn = c.SchemaNode(c.Str(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                date_format_js=df.formats[int(self.field.get_option \
                    ('input_date_format'))]['js'],
                date_format_py=df.formats[int(self.field.get_option \
                    ('input_date_format'))]['py'],
                description=self.field.description, widget=widget,
                calendar_config=calendar_config_json,
                validator=date_validation,
                **default)
        else:
            sn = c.SchemaNode(c.Str(), title=self.field.label,
                name='input-{0}'.format(self.field.id),
                missing=c.null,
                date_format_js=df.formats[int(self.field.get_option \
                    ('input_date_format'))]['js'],
                date_format_py=df.formats[int(self.field.get_option \
                    ('input_date_format'))]['py'],
                description=self.field.description, widget=widget,
                calendar_config=calendar_config_json,
                validator=date_validation,
                **default)
        return sn

    def save_data(self, entry, value):
        if value != c.null:
            self.data = DateData()
            self.data.field_id = self.field.id
            self.data.entry_id = entry.id
            self.data.value = datetime.strptime(value,
                    df.formats[int(self.field.get_option \
                        ('input_date_format'))]['py'])
            sas.add(self.data)

    def validate_and_save(self, options):
        # TODO: This method is here because EmailField currently has no
        # Python validation. To correct this, you have 2 options:
        # 1. Create an EditSchema inner class and delete this method,
        #    activating the superclass' method through inheritance.
        # 2. Simply implement this method differently if the above option is
        #    insufficient for this field's needs.
        return self.save_options(options)

    def save_options(self, options):
        '''Persists field properties.'''
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        self.save_option('month_selector', options['month_selector'])
        self.save_option('year_selector', options['year_selector'])
        self.save_option('show_week', options['show_week'])
        self.save_option('input_date_format', options['input_date_format'])
        self.save_option('export_date_format', options['export_date_format'])
        # "default" is a reserved word in javascript. Gotta change that name:
        self.save_option('defaul', options['defaul'])

    def schema_options(self):
        pass

    def to_dict(self, to_export=False):
        d = dict(
            type=self.field.typ.name,
            label=self.field.label,
            field_id=self.field.id,
            required=self.field.required,
            input_date_format=self.field.get_option('input_date_format'),
            export_date_format=self.field.get_option('export_date_format'),
            month_selector=True if self.field.get_option('month_selector') == 'true' else False,
            year_selector=True if self.field.get_option('year_selector') == 'true' else False,
            show_week=True if self.field.get_option('show_week') == 'true' else False,
            description=self.field.description,
            defaul=self.field.get_option('defaul'),
        )
        return d
