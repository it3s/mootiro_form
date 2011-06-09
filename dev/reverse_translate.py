#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Replaces the translation strings in source code with those of an
existing .po file, so you can use a .po file to alter translation strings.

Call like this:
./reverse_translate.py -i ../src/mootiro_form/locale/en/LC_MESSAGES/mootiro_form.po -o ../src/mootiro_form -e "js py tmpl.html po genshi" > report.txt
'''

from __future__ import unicode_literals  # unicode by default
import codecs
from unipath import Path
from mootiro_web.transecma import po2dict


class ReverseTranslator(object):
    def __init__(self, ipath, encoding='utf8',
                 keywords='_ tr ugettext gettext'):
        self.encoding = encoding
        self.replacers = ["{}('{{}}')".format(k) for k in keywords.split()]
        self.replacers.extend(
                         ['{}("{{}}")'.format(k) for k in keywords.split()]
        )
        self._read_input(ipath)
        self.found = []

    def _read_input(self, path):
        with codecs.open(path, encoding=self.encoding) as stream:
            d = po2dict(stream, 'en')
        del d['']
        # Remove items in which key is identical to value (no translation)
        # Also change line breaks into \n
        self.translations = {k: v.replace('\n', '\\n') \
            for k, v in d.items() if k != v}

    def replace_in_file(self, path):
        with codecs.open(path, encoding=self.encoding) as stream:
            content = stream.read()
        for original, translation in self.translations.items():
            old_content = content
            if path.endswith('.genshi') or path.endswith('.po'):
                content = content.replace(original, translation)
            else:
                for k in self.replacers:
                    content = content.replace \
                        (k.format(original), k.format(translation))
            if old_content != content:
                self.found.append(original)
        with codecs.open(path, 'w', encoding=self.encoding) as writer:
            writer.write(content)

    def replace_in_dir(self, dir, extensions):
        # pattern = '*.{}'.format(extension)
        extensions = ['.' + e for e in extensions.split()]
        def filter(path):
            for e in extensions:
                if path.endswith(e):
                    return True
            return False
        for path in Path(dir).walk(filter=filter):
            print(path)
            self.replace_in_file(path)

    def report_found(self):
        found = set(self.found)
        print('\nFound and replaced these strings:')
        for f in found:
            print(f)
        print('')
        original = set(self.translations.keys())
        missed = original - found
        print('\nMissed these strings:')
        for m in missed:
            print(m)



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Changes source code based on a .po file.')
    p.add_argument('-i', '--input', dest='input_path', metavar='FILE',
        help='path to the input .po file')
    p.add_argument('-e', '--extensions', dest='extensions', metavar='EXTENSION',
        help='file extensions to consider (default: py)', default='py')
    p.add_argument('-o','--output-dir',  dest='out_dir', metavar='DIR',
                   help="directory containing source code to change")
    n = p.parse_args()
    r = ReverseTranslator(n.input_path)
    # r.replace_in_file('../src/mootiro_form/views/user.py')
    r.replace_in_dir(n.out_dir, n.extensions)
    r.report_found()
