#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Serves MootiroForm using the high-performance CherryPy WSGI server.
(I don't think the Paste http server is very good,
it has been printing mysterious error messages on the console.)

Before running this script, install CherryPy 3.2 or later:

    easy_install -UZ cherrypy

'''

from __future__ import unicode_literals  # unicode by default
from cherrypy.wsgiserver import CherryPyWSGIServer
from pyramid.paster import get_app

app = get_app('development.ini', 'mootiro_form')
port = 6545
server = CherryPyWSGIServer(('0.0.0.0', port), app, numthreads=10, max=10,
    request_queue_size=200, timeout=120,
)

if __name__ == '__main__':
    print('Running MootiroForm under CherryPy on http://localhost:{}/' \
        .format(port))
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit) as e:
        server.stop()
        print('\nStopping CherryPy server.')
