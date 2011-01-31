#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://docs.python.org/whatsnew/pep-328.html
from __future__ import absolute_import
from __future__ import print_function   # deletes the print statement
from __future__ import unicode_literals # unicode by default

# http://peak.telecommunity.com/DevCenter/setuptools#developer-s-guide

import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

install_requires = [
    'pyramid >= 1.0',
    'pyramid_handlers',
    'Babel',
    'SQLAlchemy >= 0.6.6',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
    'pyramid_beaker >= 0.2', # for sessions
    'Genshi >= 0.6', # can be exchanged for pyramid_chameleon_genshi or Kajiki
    'deform >= 0.8.1',
    'mootiro_web',
]

if sys.version_info[:3] < (2,5,0):
    install_requires.append('pysqlite')

setup(name='mootiro_form',
    version='0.0',
    description='A web tool that lets you create forms, collect ' \
                'information and generate reports',
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='the IT3S team',
    author_email='team@it3s.org',
    url='http://mootiro.org/',
    keywords='web forms wsgi pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='mootiro_form',
    install_requires = install_requires,
    # Download the development version of mootiro_web:
    dependency_links = ['https://github.com/it3s/mootiro_web/tarball/master' \
                        '#egg=mootiro_web-0.1a1'
    ],
    entry_points = """\
        [paste.app_factory]
        main = mootiro_form:main
        """,
    paster_plugins=['pyramid'],
    message_extractors = { '.': [
        ('static/**', 'ignore', None),
        ('**.py', 'python', None),
        #('**.py', 'chameleon_python', None),
        ('**.pt', 'chameleon_xml', None),
        ('**.genshi', 'genshi', None),
        #('**.genshi', 'genshi', 'include_attrs = title'),
        # http://genshi.edgewall.org/wiki/Documentation/i18n.html
    ]},
)
