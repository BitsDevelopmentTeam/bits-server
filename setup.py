#!/usr/bin/env python
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from distutils.core import setup

setup(
    name='bitsd',
    version='2.1',
    description='Presence server, logger and remote listener.',
    author='Stefano Sanfilippo et al.',
    author_email='a.little.coder@gmail.com',
    url='https://github.com/esseks/bitsd',
    packages=[
        'bitsd',
        'bitsd.client',
        'bitsd.listener',
        'bitsd.listener.remote',
        'bitsd.persistence',
        'bitsd.persistence.logger',
        'bitsd.persistence.pages',
        'bitsd.server',
        'bitsd.server.http',
        'bitsd.server.http.templates',
        'bitsd.server.websockets',
    ],
    scripts=[
        'bitsd.py'
    ],
    package_data={
        'bitsd.server.http': [
            '*.html',
            'assets/*',
        ],
        'bitsd.server.http.templates': [
            '*.html'
        ]
    }
)