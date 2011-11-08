#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://peak.telecommunity.com/DevCenter/setuptools#developer-s-guide

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, '../README.md')).read()
CHANGES = open(os.path.join(here, '../doc/CHANGES.txt')).read()

install_requires = [
    'Babel',
    'pyramid >= 1.2',
    'pyramid_handlers',
    'pyramid_beaker >= 0.2',  # for sessions
    'repoze.tm2',
    'SQLAlchemy >= 0.7.1',
    'sqlalchemy-migrate >= 0.7.1',
    'transaction',
    'zope.sqlalchemy',
    'WebError',
    #  'lxml',  # this can be hard to compile, maybe it is best to apt-get it
    'Genshi >= 0.6',  # can be exchanged for pyramid_chameleon_genshi or Kajiki
    'deform >= 0.9',
    'colander == 0.9.4',
    'mootiro_web',
    'TurboMail',
    'lingua',
]

setup(name='mootiro_form',
    version='1.0beta1',
    url='https://github.com/it3s/mootiro_form',
    download_url='https://github.com/it3s/mootiro_form/downloads',
    description='A web tool that lets you create forms, collect ' \
                'information and generate reports',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='the IT3S team',
    author_email='team@it3s.org',
    keywords='web forms pyramid',
    packages=find_packages(),
    package_data = {'mootiro_form': [
        'locale/*.pot',
        'static/js/i18n/*',
        'static/js/url.js',
        '*.txt',
    ]},
    include_package_data=True,
    zip_safe=False,
    test_suite='mootiro_form',
    install_requires=install_requires,
    # Download the development version of mootiro_web:
    dependency_links=['https://github.com/it3s/mootiro_web/tarball/master' \
                      '#egg=mootiro_web-0.1a1',
                      # TODO: This is not being downloaded:
                      'https://github.com/nandoflorestan/' \
                      'colander/tarball/master#egg=colander-0.9.2',
    ],
    entry_points="""
        [paste.app_factory]
        main = mootiro_form:main
        """,
    paster_plugins=['pyramid'],
    message_extractors={'.': [
        ('static/**', 'ignore', None),
        ('**.py', 'python', None),
        #('**.py', 'lingua_python', None),
        ('**.pt', 'lingua_xml', None),
        ('**.genshi', 'genshi', None),
        #('**.genshi', 'genshi', 'include_attrs = title'),
        # http://genshi.edgewall.org/wiki/Documentation/i18n.html
    ]},
)
