#! /usr/bin/env python
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Fill Database with Markdown pages.
"""

# DO NOT REMOVE
import bitsd.properties

from bitsd.persistence import start
from bitsd.persistence.models import Page
from bitsd.persistence.engine import persist, session_scope
from tornado.options import parse_config_file


if __name__ == '__main__':
    try:
        parse_config_file('/etc/bitsd.conf')
    except IOError:
        print ("No /etc/bitsd.conf found, ignoring.")

    start()

    with open('INFO.md', 'r') as info:
        infopage = Page('Info', info.read().decode('utf-8'))
        with session_scope() as session:
            persist(session, infopage)
