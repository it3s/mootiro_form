#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Script that prepares files for internationalization.

Call it as:  translate_mf.py -1
...then edit the .po files, maybe using poedit,
...then call:  translate_mf.py -2
...to compile the translations.

To create a new .po file (for a new locale), issue this command:

    pybabel init -D $DOMAIN -i $POTFILE -d $OUTDIR -l $LOCALE

...and then update the end of this script.
'''

from __future__ import unicode_literals  # unicode by default

from os.path import join
from subprocess import call, check_call
# http://babel.edgewall.org/wiki/Documentation/0.9/cmdline.html


class BaseTranslator(object):
    '''This class is reusable in future applications.'''
    def __init__(self):
        self.steps1 = [('./setup.py', 'extract_messages')]
        self.steps2 = [('./setup.py', 'update_catalog')]
        self.steps3 = [('./setup.py', 'compile_catalog')]

    def recreate_pots(self):
        print("\nRegenerating .pot files:\n")
        self.make_calls(self.steps1)

    def make_calls(self, commands):
        for command in commands:
            # print(' '.join(command))
            result = call(command)
            if result != 0:
                print('Error!')
                import sys
                sys.exit(result)

    def update(self):
        print('\nUpdating the .po files:')
        self.make_calls(self.steps2)

    def compile(self):
        print('\nCompiling the translations to make them available to the ' \
            'application:\n')
        self.make_calls(self.steps3)

    def ui(self):
        from argparse import ArgumentParser
        p = ArgumentParser(description= \
            'Performs i18n tasks for a web application.')
        p.add_argument('-T', '--nopot', dest='pot', default=True,
                       action='store_false',
                       help="Do not recreate POT files (default false)")
        p.add_argument('-U', '--noupdate', dest='po', default=True,
                       action='store_false',
                       help='Do not update PO files (default false)')
        p.add_argument('-C', '--nocompile', dest='mo', default=True,
                       action='store_false',
                       help='Do not compile translations (default false)')
        p.add_argument('-1', '--start', dest='start', default=False,
                       action='store_true',
                       help='Recreate POT files, then update PO files')
        p.add_argument('-2', '--finish', dest='finish', default=False,
                       action='store_true',
                       help='Only compile translations')
        d = p.parse_args()
        if d.start:
            d.pot = True
            d.po = True
            d.mo = False
        elif d.finish:
            d.pot = False
            d.po = False
            d.mo = True
        if d.pot:
            self.recreate_pots()
        if d.po:
            self.update()
        if d.mo:
            self.compile()


class Job(object):
    '''In addition to pybabel, this requires the po2json command from the
    Python egg mootiro_web.
    '''
    def __init__(self, dir, domain, locale=None):
        self.dir = dir
        self.domain = domain
        self.locale = locale
        self.static_dir = join(dir, 'static')
        self.js_dir = join(dir, 'static/js/i18n')
        self.locdir = join(dir, 'locale')
        self.pot = join(self.locdir, domain + '.pot')
        if locale:
            self.outdir = join(self.locdir, locale, 'LC_MESSAGES')
            self.po = join(self.outdir, domain + '.po')
            self.mo = join(self.outdir, domain + '.mo')

    def step1(self):
        '''Returns the command args to extract messages into .pot.'''
        return ('pybabel', 'extract', '-k', 'tr', '--omit-header',
                '-F', join(self.locdir, 'js_mapping.conf'),
                '-w', '100', '--sort-by-file',
                '-o', self.pot,
                self.static_dir,
        )

    def step2(self):
        '''Returns the command args to update a .po catalog.'''
        return ('pybabel', 'update', '-D', self.domain, '-i', self.pot,
            '-d', self.locdir, '-N', '-l', self.locale)

    def js_compile(self):
        '''Returns the command args to compile to javascript.'''
        return ('po2json', '-D', self.domain, '-d', self.locdir,
                '-o', self.js_dir, '-n', 'mfTranslations', '-i')


class MFTranslator(BaseTranslator):
    '''Specific to Mootiro Form.'''
    def __init__(self, dir, domains, locales):
        super(MFTranslator, self).__init__()
        self.domains = domains
        self.dir = dir
        for domain in domains:
            job = Job(dir, domain)
            self.steps1.append(job.step1())
            if domain == 'js_mf':
                self.steps3.append(job.js_compile())
        for locale in locales:
            for domain in domains:
                job = Job(dir, domain, locale)
                self.steps2.append(job.step2())


if __name__ == '__main__':
    MFTranslator(dir='mootiro_form', domains=['js_mf'],
                 locales=['en', 'pt_BR']).ui()
