#! /usr/bin/python3
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from setuptools import setup

setup(
    name='bitsd',
    version='2.1',
    license='GPLv3',
    description='Presence server, logger and remote listener.',
    author='Stefano Sanfilippo et al.',
    author_email='a.little.coder@gmail.com',
    url='https://github.com/esseks/bitsd',
    install_requires=[
        'tornado >= 2.3',
        'sqlalchemy >= 0.7',
        'markdown',
        'futures',
        'pycares',
        'passlib'
    ],
    packages=[
        'bitsd',
        'bitsd.client',
        'bitsd.listener',
        'bitsd.persistence',
        'bitsd.server',
        'bitsd.test',
    ],
    scripts=[
        'bitsd.py'
    ],
    package_data={
        'bitsd.server': [
            'templates/*.html',
            'assets/*',
            'assets/lib/*'
        ],
    },
    data_files=[
        ('etc', [
            'bitsd.conf'
        ])
    ]
)
