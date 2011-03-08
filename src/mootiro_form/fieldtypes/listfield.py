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
                        required=False)

    def value(self, entry):
        data = sas.query(ListData).join(ListOption) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListData.entry_id == entry.id).one()

        return data.list_option.label if data else ''

    def get_schema_node(self):
        title = self.field.label
        list_type = self.field.get_option('list_type')
        valuesObjs = sas.query(ListOption).filter(ListOption.field_id == self.field.id) \
                        .order_by(ListOption.position).all()


        values_tup = [(v.id, v.label) for v in valuesObjs]
        if self.field.get_option('sort_choices') == 'random':
            random.shuffle(values_tup)
        values = tuple(values_tup)

        if list_type == 'select':
            options =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True) \
                    .all()

            options_id = [o.id for o in options]

            return c.SchemaNode(c.Str(), title=title,
                            name='input-{0}'.format(self.field.id),
                            widget=d.widget.SelectWidget(
                                values=values,
                                template='form_select'), options_id=options_id,
                                multiple=self.field.get_option('multiple_choice'))

        elif list_type == 'radio':
            option =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True).first()

            return c.SchemaNode(c.Str(), title=title,
                            name='input-{0}'.format(self.field.id),
                            default=option.id,
                            missing=option.id,
                            widget=d.widget.RadioChoiceWidget(
                            template='form_radio_choice',
                            values=values),
                            opt_default=option.id)


    def save_data(self, entry, value):
        self.data = ListData()
        # TODO: Check if is a valid value
        self.data.value = value
        self.data.entry_id = entry.id
        self.data.field_id = self.field.id
        sas.add(self.data)

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
            options=list_options,
            required=self.field.required,
            defaul=self.field.get_option('defaul'),
            description=self.field.description,
        )
