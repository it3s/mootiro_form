# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import json
import csv
import deform as d
import colander as c

from cStringIO import StringIO
from pyramid.httpexceptions import HTTPFound
from pyramid_handlers import action
from pyramid.response import Response
from pyramid.renderers import render
from mootiro_form.utils.form import make_form
from pyramid.view import view_config
from mootiro_form import _
from mootiro_form.models import Form, FormCategory, FormTemplate, Field, \
                                FieldType, Entry, sas
from mootrio_form.models.entry import pagination
from mootiro_form.schemas.form import form_schema, \
                                      form_name_schema
from mootiro_form.views import BaseView, authenticated, safe_json_dumps, \
        print_time
from mootiro_form.schemas.form import create_form_schema
from mootiro_form.fieldtypes import all_fieldtypes, fields_dict, \
                                    FieldValidationError


def pop_by_prefix(prefix, adict):
    '''Pops information from `adict` if its key starts with `prefix` and
    returns another dictionary.
    '''
    prefix_length = len(prefix)
    d = {}
    for k in adict:
        if k.startswith(prefix):
            d[k[prefix_length:]] = adict.pop(k)
    return d


def extract_dict_by_prefix(prefix, adict):
    '''Reads information from `adict` if its key starts with `prefix` and
    returns another dictionary.
    '''
    prefix_length = len(prefix)
    return dict(((k[prefix_length:], v) for k, v in adict.items() \
                 if k.startswith(prefix)))


@view_config(context=FieldValidationError, renderer='json')
def field_validation_error(exception, request):
    '''This view is called when a FieldValidationError is raised from a
    field's validate_and_save() method (when saving a form).
    '''
    # TODO: log(exception.get_log_message() + '\n' + unicode(exception)),
    # maybe even send an e-mail,
    # because field validation errors are usually programming errors.
    # For now, we just print
    print(exception.get_log_message())
    return dict(field_validation_error=unicode(exception))



class FormView(BaseView):
    """The form editing view."""
    CREATE_TITLE = _('New form')
    EDIT_TITLE = _('Edit form')

    @property
    def _pagetitle(self):
        id = self.request.matchdict['id']
        return self.CREATE_TITLE if id == 'new' else self.EDIT_TITLE

    @action(name='edit', renderer='form_edit.genshi', request_method='GET')
    # @print_time('show_edit()')
    @authenticated
    def show_edit(self):
        '''Displays the form editor, for new or existing forms.'''
        form_id = self.request.matchdict['id']
        fields_config_json = json.dumps({ft[0]: ft[1](Field()).initJson() \
                                         for ft in fields_dict.items()})
        if form_id == 'new':
            form = Form()
            fields_json = json.dumps([])
        else:
            form = self._get_form_if_belongs_to_user(form_id=form_id)
            fields_json = safe_json_dumps([f.to_dict() for f in form.fields])
            # (indent=1 causes the serialization to be much prettier.)
        dform = d.Form(form_schema, formid='FirstPanel') \
            .render(self.model_to_dict(form, ('name', 'description',
                    'submit_label')))

        # TODO: Consider a caching alternative; this query might be
        # too expensive to stay in this view.
        # List of all system templates
        system_templates = sas.query(FormTemplate) \
            .filter(FormTemplate.system_template_id != None) \
            .order_by(FormTemplate.system_template_id).all()

        # Field types class names
        fieldtypes_json = json.dumps([typ.__class__.__name__ \
                                    for typ in all_fieldtypes])
        return dict(pagetitle=self._pagetitle, form=form, dform=dform,
                    action=self.url('form', action='edit', id=form_id),
                    system_templates=system_templates,
                    fields_json=fields_json, all_fieldtypes=all_fieldtypes,
                    fieldtypes_json=fieldtypes_json,
                    fields_config_json=fields_config_json)

    @action(name='edit', renderer='json', request_method='POST')
    @authenticated
    def save_form(self):
        '''Responds to the AJAX request and saves a form with its fields.'''
        request = self.request
        # TODO: Clean the posted json from malicious attacks such as XSS
        posted = json.loads(request.POST.pop('json'))
        # Validate the form panel (especially form name length)
        # TODO: Using deform for this was a mistake. We should use colander
        # only, and display errors using javascript, as we did on the
        # following method "rename".
        form_props = [('_charset_', ''),
            ('__formid__', 'FirstPanel'),
            ('name', posted['form_title']),
            ('description', posted['form_desc']),
            ('submit_label', posted['submit_label'])
        ]
        dform = d.Form(form_schema, formid='FirstPanel')
        try:
            dform.validate(form_props)
        except d.ValidationFailure as e:
            # print(e.args, e.cstruct, e.error, e.field, e.message)
            return dict(panel_form=e.render(),
                        error=_('Form properties error'))
        # the form panel is validated and should always be returned
        panel_form = dform.render(form_props)

        # Validation passes, so create or update the form.
        form_id = posted['form_id']
        if form_id == 'new':
            form = Form(user=request.user)
            sas.add(form)
        else:
            form = self._get_form_if_belongs_to_user(form_id=form_id)
            if not form:
                return dict(error=_('Form not found!'))

        # Form Tab Info
        form.name = posted['form_title']
        form.description = posted['form_desc']
        form.submit_label = posted['submit_label']

        # Visual Tab Info
        st_id = posted['system_template_id']
        if st_id:
            st = sas.query(FormTemplate). \
                filter(FormTemplate.system_template_id == st_id).first()
            form.template = st

        if form_id == 'new':  # TODO: really necessary anymore?
            sas.flush()  # so we get the form id

        # Get field positions
        positions = {f[:-len("_container")]: p for p, f in \
                            enumerate(posted['fields_position'])}

        # Save/Update the fields
        # Fields to delete
        for f_id in posted['deleteFields']:
            # TODO: check what to do with the field answer data!!!
            field = sas.query(Field).join(Form).filter(Field.id == f_id)\
                        .filter(Form.user_id == request.user.id).first()
            sas.delete(field)

        new_fields_id = {}
        save_options_result = {}
        for f in posted['fields']:
            if not f['field_id']:
                raise RuntimeError('Cannot instantiate a field of ID {}' \
                    .format(f['field_id']))
            elif f['field_id'] == 'new':
                field_type = sas.query(FieldType) \
                    .filter(FieldType.name == f['type']).first()
                # To solve a bug where field.save_options() would fail because
                # of a missing field ID, we instantiate the field here and flush
                field = Field(typ=field_type, form=form, label=f['label'],
                    description=f['description'], help_text=None)
                sas.add(field)
                sas.flush()
                # TODO: Populating the above instance variables is probably
                # redundantly done elsewhere, but it must be done here.
            else:
                field = sas.query(Field).get(f['field_id'])
                if not field:
                    return dict(error=_("Field not found: {}") \
                        .format(f['field_id']))

            f['position'] = positions[f['id']]
            # Before the following call, the field must have an ID.
            # If the following line raises a FieldValidationError, Pyramid will
            # call the field_validation_error action.
            result = field.validate_and_save(f)
            if result:
                save_options_result[f['id']] = result

            # If is a new field, need to inform the client about
            # the field id on DB after a flush
            if f['field_id'] == 'new':
                sas.flush()
                new_fields_id[f['id']] = {'field_id': field.id}

        rdict = {'form_id': form.id,
                'new_fields_id': new_fields_id,
                'save_options_result': save_options_result,
                'panel_form': panel_form,
                }
        return rdict

    def _get_form_if_belongs_to_user(self, form_id=None, key='id'):
        '''Returns the form instance indicated by matchdict[key],
        as long as it belongs to the current user.
        '''
        if not form_id:
            form_id = self.request.matchdict[key]
        return sas.query(Form).filter(Form.id == form_id) \
            .filter(Form.user == self.request.user).first()

    @action(renderer='json', request_method='POST')
    @authenticated
    def rename(self):
        # 1. Validate form name length, using only Colander
        new_name = self.request.POST['form_name']
        try:
            form_name_schema.deserialize(new_name)
        except c.Invalid as e:
            return e.asdict()  # {'name': u'Longer than maximum length 255'}
        # 2. Retrieve the form model
        form = self._get_form_if_belongs_to_user()
        if not form:
            return dict(name=_("Error finding form"))
        # 3. Save the new name, return OK
        form.name = new_name
        return {'name': ''}

    @action(renderer='json', request_method='POST')
    @authenticated
    def delete(self):
        form = self._get_form_if_belongs_to_user()
        if form:
            sas.delete(form)
            sas.flush()
            error = ''
        else:
            error = _("This form doesn't exist!")
        user = self.request.user
        all_data = user.all_categories_and_forms()
        return {'errors': error, 'all_data': all_data}

    @action(name='copy', renderer='json', request_method='POST')
    @authenticated
    def copy(self):
        form = self._get_form_if_belongs_to_user()
        if form:
            form_copy = form.copy()
            form_copy.name += " " + _("(copy)")
            sas.flush()
            error = ''
        else:
            error = _("This form doesn't exist!")

        user = self.request.user
        all_data = user.all_categories_and_forms()
        return {'errors': error, 'all_data': all_data,
            'form_copy_id': form_copy.id}

    def _get_schema_and_form(self, form):
        form_schema = create_form_schema(form)
        entry_form = make_form(form_schema, i_template='form_mapping_item',
            buttons=[form.submit_label if form.submit_label else _('Submit')],
            action=(self.url('form', action='view', id=form.id)))
        return form_schema, entry_form

    @action(name='view', renderer='form_view.genshi')
    @authenticated
    def view(self):
        form = self._get_form_if_belongs_to_user()

        form_schema, entry_form = self._get_schema_and_form(form)
        form_data = self.request.params.items()

        if self.request.method == "POST":
            try:
                form_data = entry_form.validate(form_data)
            except d.ValidationFailure as e:
                return dict(entry_form=e.render(), form=form)

        return dict(entry_form=entry_form.render(), form=form)

    @action(name='template')
    def css_template(self):
        '''Returns a file with css rules for the entry creation form.'''
        form = self._get_form_if_belongs_to_user()
        fonts, colors = form.template.css_template_dicts()
        #render the template as string to return it in the body of the response
        tpl_string = render('entry_creation_template.mako',
                             dict(f=fonts, c=colors), request=self.request)
        return Response(status='200 OK',
               headerlist=[(b'Content-Type', b'text/css')],
               body=tpl_string)

    @action(name='category_show_all', renderer='category_show.genshi',
            request_method='GET')
    @authenticated
    def category_show(self):
        categories = sas.query(FormCategory).all()
        return categories

    @action(name='answers', renderer='form_answers.genshi')
    @authenticated
    def answers(self):
        '''Displays a list of the entries of a form.'''
        form_id = int(self.request.matchdict['id'])
        form = self._get_form_if_belongs_to_user(form_id)
        # Get the answers
        #print pagination(form_id, 1, 3)[2].entry_number
        #print pagination(form_id, 2, 3)[0].entry_number
        #print pagination(form_id, 2, 3)[1].entry_number
        return dict(form=form, entries=form.entries, form_id=form.id)

    @action(renderer='json')
    @authenticated
    def entry_list(self, page=1, limit=2):
        # TODO: Write correct description
        '''Displays a list of the entries of a form.'''
        form_id = int(self.request.matchdict['id'])
        # TODO: if not form:
        # Get the answers
        entries = [e.to_dict() for e in pagination(form_id, page, limit)]
        return entries


    def _csv_generator(self, form_id, encoding='utf-8'):
        '''A generator that returns the entries of a form line by line.
        '''
        form = sas.query(Form).filter(Form.id == form_id).one()
        file = StringIO()
        csvWriter = csv.writer(file, delimiter=b',',
                         quotechar=b'"', quoting=csv.QUOTE_NONNUMERIC)
        # write column names
        column_names = [self.tr(_('Entry')).encode(encoding),
                        self.tr(_('Submissions (Date, Time)')) \
                                  .encode(encoding)] + \
                       [f.label.encode(encoding) for f in form.fields]
        csvWriter.writerow(column_names)
        for e in form.entries:
            # get the data of the fields of the entry e in a list
            fields_data = [e.entry_number, str(e.created)[:16]] + \
                          [f.value(e).encode(encoding) for f in form.fields]
            # generator which returns one row of the csv file (=data of the
            # fields of the entry e)
            csvWriter.writerow(fields_data)
            row = file.getvalue()
            file.seek(0)
            file.truncate()
            yield row
        sas.remove()

    @action(name='export', request_method='GET')
    @authenticated
    def create_csv(self):
        '''Exports the entries to a form as csv file and initializes
        download from the server.
        '''
        form = self._get_form_if_belongs_to_user()
        # Assign name of the file dynamically according to form name and
        # creation date. Have to cut the name to have a max filename lenght
        # of 255 Characters. More is not supported by the os.
        name = self.tr(_('Entries_to_{0}_{1}.csv')) \
                .format(unicode(form.name[:200]).replace(' ','_'),
                        unicode(form.created)[:10])
        # Initialize download while creating the csv file by passing a
        # generator to app_iter. To avoid SQL Alchemy session problems sas is
        # called again in csv_generator instead of passing the form object
        # directly.
        return Response(status='200 OK',
               headerlist=[(b'Content-Type', b'text/comma-separated-values'),
                    (b'Content-Disposition', b'attachment; filename={0}' \
                    .format(name.encode('utf8')))],
               app_iter=self._csv_generator(form.id))
