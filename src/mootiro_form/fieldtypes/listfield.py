# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import random
import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.list_data import ListOption, ListData
from mootiro_form.models.field_option import FieldOption


class ListField(FieldType):
    name = _('List input')
    brief = _("List of options to select one or more.")
    model = ListData

    defaultValue = dict(defaul='',
                        list_type='select',
                        multiple_choice=False,
                        sort_choices='user_defined',
                        size_options=1,
                        new_option=False,
                        required=False,
                        export_in_columns=False)

    def value(self, entry):
        data = sas.query(ListOption).join(ListData) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListData.entry_id == entry.id) \
                    .filter(ListOption.id == ListData.value).all()
        values = ""
        if data:
            for a in data[:-1]:
                values += a.label
                values += ", "
            values += data[-1].label

        return values

    def get_schema_node(self):
        title = self.field.label
        list_type = self.field.get_option('list_type')
        sort_choices = self.field.get_option('sort_choices')
        valuesQuery = sas.query(ListOption).filter(ListOption.field_id == self.field.id)

        if sort_choices == 'user_defined':
            valuesObjs = valuesQuery.order_by(ListOption.position).all()
            values_tup = [(v.id, v.label) for v in valuesObjs]
        elif sort_choices == 'random':
            valuesObjs = valuesQuery.all()
            values_tup = [(v.id, v.label) for v in valuesObjs]
            random.shuffle(values_tup)
        elif sort_choices == 'alpha_asc':
            valuesObjs = valuesQuery.order_by(ListOption.label).all()
            values_tup = [(v.id, v.label) for v in valuesObjs]
        elif sort_choices == 'alpha_desc':
            valuesObjs = valuesQuery.order_by(ListOption.label.desc()).all()
            values_tup = [(v.id, v.label) for v in valuesObjs]

        values = tuple(values_tup)

        # Create the Mapping for select field
        list_map_schema = c.SchemaNode(c.Mapping(), name='input-{0}'.format(self.field.id),
                            widget=d.widget.MappingWidget(template='form_select_mapping'))

        if list_type == 'select':
            options =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True) \
                    .all()

            options_id = [o.id for o in options]

            def_dict = {}
            if not self.field.required:
                def_dict = {'missing': c.null, 'default': c.null}

            list_schema = c.SchemaNode(d.Set(allow_empty=not self.field.required), title=title,
                    name='option',
                    widget=d.widget.SelectWidget(
                        values=values,
                        template='form_select'),
                        defaults=options_id,
                        multiple=self.field.get_option('multiple_choice'),
                        **def_dict)

        elif list_type == 'radio':
            option =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True).first()

            if option:
                default_id = option.id
            else:
                default_id = ''

            req_dict = {}
            if not self.field.required:
                req_dict = {'missing': c.null, 'default': c.null}

            list_schema = c.SchemaNode(d.Set(allow_empty=not self.field.required), title=title,
                        name='option',
                        widget=d.widget.RadioChoiceWidget(
                            template='form_radio_choice',
                            values=values),
                        opt_default=default_id,
                        **req_dict)

        elif list_type == 'checkbox':
            def_options =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True).all()

            req_dict = {}

            if not self.field.required:
                req_dict = {'missing': c.null, 'default': c.null}

            def_options_id = map(lambda o: o.id, def_options) if def_options else []

            list_schema = c.SchemaNode(d.Set(allow_empty=not self.field.required), title=title,
                        name='option',
                        widget=d.widget.CheckboxChoiceWidget(values=values),
                        def_options_id=def_options_id,
                        **req_dict)

        list_map_schema.add(list_schema)

        if self.field.get_option('new_option') == 'true':

            other_option = c.SchemaNode(c.Str(), title=_('Other'),
                name='other', default='', missing='',
                widget=d.widget.TextInputWidget())

            list_map_schema.add(other_option)

        return list_map_schema

    def save_data(self, entry, value):
        if value:
            if value['option'] != c.null:
                for opt in value['option']:
                    self.data = ListData()
                    # TODO: Check if is a valid value
                    self.data.value = opt
                    self.data.entry_id = entry.id
                    self.data.field_id = self.field.id
                    sas.add(self.data)

            if value.has_key('other') and value['other'] != '':
                lo = ListOption()
                lo.label = value['other']
                lo.value = lo.label
                lo.field = self.field
                sas.add(lo)
                sas.flush()

                data = ListData()
                # TODO: Check if is a valid value
                data.value = lo.id
                data.entry_id = entry.id
                data.field_id = self.field.id
                sas.add(data)

    def save_options(self, options):
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']

        # Set the field position
        self.field.position = options['position']

        # Save default value
        self.save_option('default', options['defaul'])

        # List Type
        self.save_option('list_type', options['list_type'])

        # Multiple choice
        self.save_option('multiple_choice', options['multiple_choice'])

        # Sort choices
        self.save_option('sort_choices', options['sort_choices'])

        # Number of choices
        self.save_option('size_options', options['size_options'])

        # Possible to add new option
        self.save_option('new_option', options['new_option'])

        # Export options in different columns
        self.save_option('export_in_columns', options['export_in_columns'])

        inserted_options = {}
        for option_id, opt in options['options'].items():
            if opt['option_id'] != 'new':
                lo = sas.query(ListOption).get(opt['option_id'])
                lo.label = opt['label']
                lo.value = opt['value']
                lo.opt_default = opt['opt_default']
                lo.position = opt['position']
            else:
                lo = ListOption()
                lo.label = opt['label']
                lo.value = opt['value']
                lo.opt_default = opt['opt_default']
                lo.field = self.field
                lo.position = opt['position']
                sas.add(lo)
                sas.flush()
                inserted_options[option_id] = lo.id

        # Delete options
        for list_option_id in options['deleteOptions']:
            lo = sas.query(ListOption).get(list_option_id)
            if lo:
                sas.delete(lo)

        return {'insertedOptions': inserted_options}

    def save_option(self, option, value):
        opt = sas.query(FieldOption).filter(FieldOption.option == option) \
                       .filter(FieldOption.field_id == self.field.id).first()
        if opt:
            opt.value = value
        else:
            new_option = FieldOption(option, value)
            self.field.options.append(new_option)

    def schema_options(self):
        pass

    def to_json(self):
        field_id = self.field.id
        list_optionsObj = sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .order_by(ListOption.position).all()

        list_options = [{'label':lo.label, 'value':lo.value, \
                         'opt_default': lo.opt_default,'option_id':lo.id, \
                         'position': lo.position} for lo in list_optionsObj]

        return dict(
            field_id=field_id,
            label=self.field.label,
            type=self.field.typ.name,
            list_type=self.field.get_option('list_type'),
            multiple_choice=True if self.field.get_option('multiple_choice') == 'true' else False,
            sort_choices = self.field.get_option('sort_choices'),
            size_options= self.field.get_option('size_options'),
            new_option= True if self.field.get_option('new_option') == 'true' else False,
            options=list_options,
            required=self.field.required,
            defaul=self.field.get_option('defaul'),
            export_in_columns=True if self.field.get_option('export_in_columns') == 'true' else False,
            description=self.field.description,
        )
