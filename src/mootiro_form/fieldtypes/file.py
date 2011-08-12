# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import os.path
import mimetypes

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.file_data import FileData
from mootiro_form.models.file_upload_temp_store import FileUploadTempStore

class TempStore(dict):
    """ Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface"""

    def _clear(self):
        data = sas.query(FileUploadTempStore) \
            .filter(FileUploadTempStore.created < datetime.datetime.utcnow() -
                    datetime.timedelta(minutes=30)).all()
        for d in data:
            sas.delete(d)
            path = os.path.join(self.upload_temp_dir, d.uid)
            try:
                os.remove(path)
            except OSError:
                pass # what to do if fail?

    def preview_url(self, uid):
        return '/file/image_preview/%s' % uid

    def get(self, name, default=None):
        try:
            return self.__getitem__(name)
        except AttributeError:
            return default

    def __getitem__(self, name):
        self._clear()
        data = sas.query(FileUploadTempStore) \
                .filter(FileUploadTempStore.uid == name).first()
        if not data:
            raise AttributeError, "Name '{0}' does not exists".format(name)

        value = data.to_dict()
        path = os.path.join(self.upload_temp_dir, value['uid'])
        value['preview_url'] = self.preview_url(value['uid'])
        value['path'] = path
        value['fp'] = open(path, 'rb')

        if value:
            return value
        else:
            raise AttributeError, "Name '{0}' does not exists".format(name)

    def __setitem__(self, name, value):
        if not value or not 'uid' in value:
            return

        uid = value['uid']
        if not uid:
            return

        path = os.path.join(self.upload_temp_dir, uid)

        fp = value['fp']
        if not fp or fp.closed or fp.name == path:
            return

        f = open(path, 'wb')
        try:
            f.write(fp.read())
        finally:
            f.close()
            fp.close()
        data = sas.query(FileUploadTempStore) \
                .filter(FileUploadTempStore.uid == uid).first()
        if not data:
            data = FileUploadTempStore()
        data.created = datetime.datetime.utcnow()
        data.uid = uid
        data.mimetype = unicode(value['mimetype'])
        data.filename = unicode(value['filename'])
        data.size = int(value['size'])
        sas.add(data)

tmpstore = TempStore()

class FileMimeTypes(object):
    mimetypes = []

    def add(self, desc, py, js):
        self.mimetypes.append({'desc': desc, 'py': py, 'js': js})


mt = FileMimeTypes()

class FileFieldBase(FieldType):
    name = _('File field')
    brief = _("file field")
    defaultValue = dict(maxSize=2000000, required=False)

    def initJson(self):
        return dict(image_mimetypes=map(lambda f:
            {'desc': f['desc'], 'js': f['js']}, mt.mimetypes))

    def get_widget(self):
        return d.widgets.FileUploadWidget(tmpstore,
                                          template='form_image')

    def value(self, entry):
        data = sas.query(FileData) \
                .filter(FileData.field_id == self.field.id) \
                .filter(FileData.entry_id == entry.id).first()

        if data:
            return '{url}/file/view/%d/%d' % (data.entry_id, data.field_id)
        else:
            return ''

    def path(self, entry):
        data = sas.query(FileData) \
                .filter(FileData.field_id == self.field.id) \
                .filter(FileData.entry_id == entry.id).first()

        if data:
            return data.path
        else:
            return ''

    def get_schema_node(self):
        f = self.field
        defaul = c.null
        kw = dict(title=f.label,
            name='input-{0}'.format(f.id),
            description=f.description,
            widget=self.get_widget(),
        )
        if not f.required:
            kw['missing'] = defaul

        def file_validation(node, val):
            mimetype = val['mimetype']
            size = val['size']

            is_mimetype_allowed = False
            for allowed in mt.mimetypes:
                if mimetype == allowed['py']:
                    is_mimetype_allowed = True

            if not is_mimetype_allowed:
                raise c.Invalid(node, _("Invalid file format"))

        kw['validator'] = file_validation
        return c.SchemaNode(d.FileData(), **kw)

    def save_data(self, entry, value):
        if value is c.null:
            return # There is nothing to save

        uid = value['uid']
        if not uid:
            return # Invalid value

        tmp = tmpstore.get(uid)

        if tmp and 'fp' in tmp:

            form_id = entry.form_id
            entry_number = entry.entry_number
            collector_slug = entry.collector.slug

            # Create directory hierarchy
            from mootiro_form import mkdir
            bunch_dir = os.path.join(self.upload_data_dir,
                                     '%03d' % (form_id % 1000))
            mkdir(bunch_dir)

            form_dir = os.path.join(bunch_dir,'form_%d' % form_id)
            mkdir(form_dir)

            collector_dir = os.path.join(form_dir, collector_slug)
            mkdir(collector_dir)

            start = entry_number - (entry_number % 100)
            end = start + 99
            entry_range = '%d-%d' % (start, end)
            range_dir = os.path.join(collector_dir, entry_range)
            mkdir(range_dir)

            mimetype = value['mimetype']
            original_filename = value['filename']
            extension = mimetypes.guess_extension(mimetype)

            filename = 'entry{entry_number}_field{field_id}{extension}' \
                           .format(entry_number=entry_number,
                                   field_id=self.field.id,
                                   extension=extension)

            path = os.path.join(range_dir, filename)

            # Save file
            fp = tmp['fp']
            open(path, 'wb').write(fp.read())
            size = os.path.getsize(path)

            # Save db row
            self.data = FileData()
            self.data.mimetype = unicode(mimetype)
            self.data.filename = unicode(original_filename)
            self.data.size = int(size)
            self.data.path = unicode(path)
            self.data.field_id = int(self.field.id)
            self.data.entry_id = int(entry.id)
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
        # Save the other properties
        for s in self._special_options:
            if s == 'mimeTypes' and isinstance(options.get(s, ''), dict):
                self.save_option(s, '|'.join(options.get(s, '').keys()))
            else:
                self.save_option(s, options.get(s, ''))

    def to_dict(self, to_export=False):
        field_id = self.field.id
        d = dict(
            type=self.field.typ.name,
            label=self.field.label,
            field_id=field_id,
            required=self.field.required,
            description=self.field.description,
        )
        options = sas.query(FieldOption) \
                      .filter(FieldOption.field_id == field_id).all()
        d.update({o.option: o.value for o in options})
        return d

    def before_delete(self, entry):
        try:
            os.remove(self.path(entry))
        except OSError:
            pass # what to do if fail?
