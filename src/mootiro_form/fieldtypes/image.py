# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # unicode by default

import os.path
import mimetypes

import json

import colander as c
import deform as d

from mootiro_form import _
from mootiro_form.fieldtypes import FieldType
from mootiro_form.fieldtypes.file import FileFieldBase, tmpstore
from mootiro_form.models import sas
from mootiro_form.models.field_option import FieldOption
from mootiro_form.models.file_data import FileData

def is_db_true(text):
    return text == '1' or text == 'true'

class ImageMimeTypes(object):
    mimetypes = []

    def add(self, desc, py, js):
        self.mimetypes.append({'desc': desc, 'py': py, 'js': js})


mt = ImageMimeTypes()
mt.add('.jpg, .jpeg', ['image/jpeg', 'image/pjpeg'],
               ['image/jpeg', 'image/pjpeg'])
mt.add('.png', ['image/png'],
               ['image/png'])
mt.add('.gif', ['image/gif'],
               ['image/gif'])
mt.add('.tiff', ['image/tiff'],
                ['image/tiff'])
mt.add('.bmp', ['image/bmp'],
               ['image/bmp'])
mt.add('.eps', ['image/eps', 'image/x-eps'],
               ['image/eps', 'image/x-eps'])


class ImageField(FileFieldBase):
    name = _('Image field')
    brief = _("image field")
    defaultValue = dict(maxSize=2000000, required=False)

    def initJson(self):
        return dict(image_mimetypes=map(lambda f:
            {'desc': f['desc'], 'js': f['js']}, mt.mimetypes))

    def get_widget(self):
        f = self.field
        return d.widget.FileUploadWidget(tmpstore,
             template='form_image',
             style='display:table-cell; vertical-align:middle; width:{}px; height: {}px; {}'. \
                 format(f.get_option('width'),
                        f.get_option('height'),
                        '' if is_db_true(f.get_option('showPlaceholder')) else 'display:none;' ),
             img_style='clear:both; position:relative; max-width:{}px; max-height: {}px;'. \
                 format(f.get_option('width'),
                        f.get_option('height')))

    def value(self, entry):
        data = sas.query(FileData) \
                .filter(FileData.field_id == self.field.id) \
                .filter(FileData.entry_id == entry.id).first()

        if data:
            return '{url}/file/thumbnail/%d/%d' % (data.entry_id, data.field_id)
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

        def image_validation(node, val):
            mimetype = val['mimetype']
            size = val['size']

            configured = f.get_option('mimeTypes').split('|')

            for allowed in [m for m in mt.mimetypes]:
                if allowed['desc'] in configured and mimetype in allowed['py']:
                    return

            raise c.Invalid(node, _("Invalid image format"))

        kw['validator'] = image_validation
        return c.SchemaNode(d.FileData(), **kw)

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
        d['showPlaceholder'] = is_db_true(d.get('showPlaceholder', '0'))
        types = d.get('mimeTypes', '').split('|')
        d['mimeTypes'] = {}
        for typ in types:
            if typ:
                d['mimeTypes'][typ] = True
        return d

    def save_data(self, entry, value):
        FileFieldBase.save_data(self, entry, value)

        self.save_thumbnail(entry, value)

    def save_thumbnail(self, entry, value):
        from PIL import Image
        f = self.field

        path = self.path(entry)
        thumbnail_path = path[:path.rfind('.')] + ".thumbnail.jpg"
        size = max(int(f.get_option('width')), int(f.get_option('height')))
        size = size, size

        print size

        img = Image.open(path)
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(thumbnail_path, "JPEG")

        data = sas.query(FileData) \
               .filter(FileData.field_id == f.id) \
               .filter(FileData.entry_id == entry.id).first()
        if data:
            data.thumbnail_path = thumbnail_path
            print 'salva'
            sas.add(data)

        print 'Save Thumbnail'


    _special_options = 'maxSize mimeTypes showPlaceholder height width'.split()
