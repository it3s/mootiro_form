#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://peak.telecommunity.com/DevCenter/setuptools#developer-s-guide

import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid >= 1.0a7',
    'SQLAlchemy >= 0.6.5',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
    'pyramid_beaker >= 0.2',
    'bag',
    'Genshi >= 0.6',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='formcreator',
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
      author='it3s',
      author_email='',
      url='http://mootiro.org/',
      keywords='web forms wsgi pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='formcreator',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = formcreator:main
      """,
      paster_plugins=['pyramid'],
      )

