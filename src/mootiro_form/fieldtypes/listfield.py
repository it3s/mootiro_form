# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import random
import colander as c
import deform as d
from sqlalchemy import or_

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
                        new_option_label=_('Other'),
                        moderated=True,
                        case_sensitive=True,
                        min_num=1,
                        max_num=0,
                        required=False,
                        opt_restrictions=False,
                        status='Form owner',
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
        if self.field.get_option('multiple_choice') == 'true':
            multiple_choice = True
        else:
            multiple_choice = False
        valuesQuery = sas.query(ListOption) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListOption.status != 'Rejected') \
                .filter(ListOption.status != 'Awaiting moderation')

        if sort_choices == 'user_defined':
            valuesObjs = valuesQuery.order_by(ListOption.position).all()
        elif sort_choices == 'random':
            valuesObjs = valuesQuery.all()
        elif sort_choices == 'alpha_asc':
            valuesObjs = valuesQuery.order_by(ListOption.label).all()
        elif sort_choices == 'alpha_desc':
            valuesObjs = valuesQuery.order_by(ListOption.label.desc()).all()

        values_tup = [(v.id, v.label) for v in valuesObjs]

        if sort_choices == 'random':
            random.shuffle(values_tup)

        values = tuple(values_tup)

        opt_restrictions = self.field.get_option('opt_restrictions')
        min_num = self.field.get_option('min_num')
        max_num = self.field.get_option('max_num')

        def valid_require(node, value):
            if self.field.get_option('new_option') == 'true':
                if self.field.required:
                    if list_type != 'radio':
                        print value['option']
                        if not value['option'].difference(set([''])) \
                                       and not value['other']:
                            raise c.Invalid(node, _('Required.'))
                    else:
                        if not value['option'] and not value['other']:
                            raise c.Invalid(node, _('Required.'))

            elif self.field.required:
                if list_type != 'radio':
                    if not value['option'].difference(set([''])):
                        raise c.Invalid(node, _('Required.'))
                elif not value['option']:
                    raise c.Invalid(node, _('Required.'))

        def min_choices(node, value):
            try:
                int(min_num)
            except ValueError:
                return

            if self.field.get_option('new_option') == 'true':
                add = 1 if value['other'] != '' else 0
            else:
                add = 0
            lacking_options = int(min_num) - \
                    len(value['option'].difference(set(['']))) + add
            if lacking_options > 0:
                if lacking_options == 1:
                    raise c.Invalid(node,
                            _('Please, select one more option.'))
                else:
                    raise c.Invalid(node,
                            _('Please, select {0} more options.'). \
                                    format(lacking_options))

        def max_choices(node, value):
            try:
                imax_num = int(max_num)
            except ValueError:
                return


            if self.field.get_option('new_option') == 'true':
                add = 1 if value['other'] != '' else 0
            else:
                add = 0
            excess_number = \
                    len(value['option'].difference(set(['']))) + \
                        add - imax_num
            if imax_num != 0 and excess_number > 0:
                if excess_number == 1:
                    raise c.Invalid(node,
                            _('Please, deselect one option.'))
                else:
                    raise c.Invalid(node,
                            _('Please, deselect {0} options.'). \
                                    format(excess_number))

        schema_params = {}
        if list_type == 'select' or list_type == 'checkbox':
            if opt_restrictions:
                schema_params['validator'] = c.All(valid_require,
                                                min_choices, max_choices)
                schema_params['min_num'] = min_num
                schema_params['max_num'] = max_num
            else:
                schema_params['validator'] = valid_require
        else:
            schema_params['validator'] = valid_require

        if not self.field.required:
            schema_params['missing'] = {}
            schema_params['default'] = {}

        schema_params['multiple_choice'] = multiple_choice
        # Create the Mapping for select field

        list_map_schema = c.SchemaNode(c.Mapping(),
                    title=title,
                name='input-{0}'.format(self.field.id),
                widget=d.widget.MappingWidget(template='form_select_mapping',
                                    item_template='form_select_mapping_item'),
                parent_id=self.field.id,
                opt_restrictions=self.field.get_option('opt_restrictions'),
                list_type=list_type,
                **schema_params)

        options =  sas.query(ListOption) \
                .filter(ListOption.field_id == self.field.id) \
                .filter(ListOption.opt_default == True) \
                .all()

        options_id = [o.id for o in options]

        req_dict = {'missing': '', 'default': ''}

        if list_type == 'select':
            list_schema = c.SchemaNode(d.Set(allow_empty=True), title=title,
                    name='option',
                    widget=d.widget.SelectWidget(
                        values=values,
                        template='form_select'),
                    defaults=options_id,
                    description=self.field.description,
                    multiple=self.field.get_option('multiple_choice'),
                    parent_id=self.field.id,
                    **req_dict)

        elif list_type == 'radio':
            option =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True).first()

            if option:
                default_id = option.id
            else:
                default_id = ''

            list_schema = c.SchemaNode(c.Str(), title=title,
                        name='option',
                        widget=d.widget.RadioChoiceWidget(
                            template='form_radio_choice',
                            values=values),
                        description=self.field.description,
                        opt_default=default_id,
                        parent_id=self.field.id,
                        **req_dict)

        elif list_type == 'checkbox':
            def_options =  sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.opt_default == True).all()

            list_schema = c.SchemaNode(d.Set(allow_empty=True), title=title,
                        name='option',
                        widget=d.widget.CheckboxChoiceWidget(values=values,
                            template='form_checkbox_choice'),
                        defaults=options_id,
                        description=self.field.description,
                        parent_id=self.field.id,
                        **req_dict)

        list_map_schema.add(list_schema)

        if self.field.get_option('new_option') == 'true':
            other_option_label = self.field.get_option('new_option_label')
            other_schema_args = dict( title=''
                                    , name='other'
                                    , default=''
                                    , missing=''
                                    , widget=d.widget.TextInputWidget(
                                                   template='form_other'
                                                 , category='structural')
                                    , other_label=other_option_label
                                    , list_type=list_type
                                    , parent_id=self.field.id)

            other_option = c.SchemaNode(c.Str(), **other_schema_args)
            list_map_schema.add(other_option)

        return list_map_schema

    def save_data(self, entry, value):
        list_type = self.field.get_option('list_type')

        if value:
            if value['option'] and value['option'] != c.null:
                if list_type != 'radio':
                    for opt in filter(lambda o: o != '', value['option']):
                        self.data = ListData()
                        # TODO: Check if is a valid value
                        self.data.value = opt
                        self.data.entry_id = entry.id
                        self.data.field_id = self.field.id
                        sas.add(self.data)
                else:
                    self.data = ListData()
                    # TODO: Check if is a valid value
                    self.data.value = value['option']
                    self.data.entry_id = entry.id
                    self.data.field_id = self.field.id
                    sas.add(self.data)

            if value.has_key('other') and value['other'] != '':
                moderated = self.field.get_option('moderated')
                case_sensitive = self.field.get_option('case_sensitive')

                if case_sensitive == 'true':
                    option = sas.query(ListOption) \
                                .filter(ListOption.label == value['other']) \
                                .filter(ListOption.field_id == self.field.id) \
                                .first()
                else:
                    option = sas.query(ListOption) \
                                .filter(ListOption.label.ilike(value['other'])) \
                                .filter(ListOption.field_id == self.field.id) \
                                .first()

                no_options = sas.query(ListOption) \
                            .filter(ListOption.field_id == self.field.id).count()

                if not option:
                    lo = ListOption()
                    lo.label = value['other']
                    lo.value = lo.label
                    lo.field = self.field
                    lo.position = no_options
                    lo.status = 'Approved' if moderated == 'false' else 'Awaiting moderation'
                    sas.add(lo)
                    sas.flush()
                else:
                    lo = option

                data = ListData()
                # TODO: Check if is a valid value
                data.value = lo.id
                data.entry_id = entry.id
                data.field_id = self.field.id
                sas.add(data)

    def validate_and_save(self, options):
        # TODO: This method is here because ListField currently has no
        # Python validation. To correct this, you have 2 options:
        # 1. Create an EditSchema inner class and delete this method,
        #    activating the superclass' method through inheritance.
        # 2. Simply implement this method differently if the above option is
        #    insufficient for this field's needs.
        return self.save_options(options)

    def save_options(self, options):
        # TODO: Validation
        self.field.label = options['label']
        self.field.required = options['required']
        self.field.description = options['description']
        self.field.position = options['position']
        self.save_option('default', options['defaul'])  # the default value

        for key in ('list_type', 'multiple_choice', 'sort_choices',
                    'new_option_label',
                    'min_num',  # minimum number of choices
                    'max_num',  # maximum number of choices
                    'size_options',     # number of choices
                    'moderated',  # other moderated
                    'new_option',  # possible to add a new option
                    'case_sensitive',  # other case sensitive
                    'opt_restrictions', # restricted number of options
                   # 'export_in_columns',  # when creating a CSV
                   ):
            self.save_option(key, options[key])

        inserted_options = {}
        for option_id, opt in options['options'].items():
            if opt['option_id'] != 'new':
                lo = sas.query(ListOption).get(opt['option_id'])
                lo.label = opt['label']
                lo.value = opt['value']
                lo.opt_default = opt['opt_default']
                lo.position = opt['position']
                # lo.status = opt['status']
                # To prevent KeyError, Nando changed the above line to:
                lo.status = opt.get('status', 'Form owner')
            else:
                lo = ListOption()
                lo.label = opt['label']
                lo.value = opt['value']
                lo.opt_default = opt['opt_default']
                lo.field = self.field
                lo.position = opt['position']
                lo.status = 'Form owner'
                sas.add(lo)
                sas.flush()
                inserted_options[option_id] = lo.id

        # Delete options
        for list_option_id in options['deleteOptions']:
            lo = sas.query(ListOption).get(list_option_id)
            if lo:
                sas.delete(lo)
        return {'insertedOptions': inserted_options}

    def schema_options(self):
        pass

    def to_dict(self):
        field_id = self.field.id

        # Approved list options
        list_optionsObj = sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(or_(ListOption.status == 'Approved', \
                        ListOption.status == 'Form owner')) \
                    .order_by(ListOption.position).all()

        # Waiting moderation list options
        list_optionsModerationObj = sas.query(ListOption) \
                    .filter(ListOption.field_id == self.field.id) \
                    .filter(ListOption.status == 'Awaiting moderation') \
                    .order_by(ListOption.position).all()

        list_options = [{'label':lo.label, 'value':lo.value, \
                         'opt_default': lo.opt_default,'option_id':lo.id, \
                         'position': lo.position,
                         'status': lo.status} for lo in list_optionsObj]

        list_options_moderation = [{'label':lo.label, 'value':lo.value, \
                     'opt_default': lo.opt_default,'option_id':lo.id, \
                     'position': lo.position,
                     'status': lo.status} for lo in list_optionsModerationObj]

        return dict(
            field_id=field_id,
            label=self.field.label,
            type=self.field.typ.name,
            list_type=self.field.get_option('list_type'),
            multiple_choice=True if self.field.get_option('multiple_choice') \
                == 'true' else False,
            sort_choices = self.field.get_option('sort_choices'),
            size_options= self.field.get_option('size_options'),
            min_num=self.field.get_option('min_num'),
            max_num=self.field.get_option('max_num'),
            new_option= True if self.field.get_option('new_option') == 'true' \
                else False,
            new_option_label=self.field.get_option('new_option_label'),
            moderated= True if self.field.get_option('moderated') == 'true' \
                else False,
            case_sensitive= True if self.field.get_option('case_sensitive') \
                == 'true' else False,
            opt_restrictions= True if self.field.get_option('opt_restrictions') \
                == 'true' else False,
            options=list_options,
            options_moderation=list_options_moderation,
            required=self.field.required,
            defaul=self.field.get_option('defaul'),
            #export_in_columns=True if \
            #    self.field.get_option('export_in_columns') == 'true' else False,
            description=self.field.description,
        )

    def copy(self, base_field):
        '''Receives base_field and copies its specific options into self.field
        options.
        Do not copy options of the field_option model, just specific ones.
        '''
        # iterate over all list options
        for base_lo in base_field.list_option:
            # option instance copy
            lo_copy = ListOption()
            lo_copy.field = self.field
            for attr in ('label', 'value', 'opt_default', 'position'):
                lo_copy.__setattr__(attr, base_lo.__getattribute__(attr))

            sas.add(lo_copy)
