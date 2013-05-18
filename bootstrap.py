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

import bitsd.properties

from bitsd.persistence import start, persist
from bitsd.persistence.pages.model import Page


if __name__ == '__main__':
    parse_config_file('/etc/bitsd.conf')

    start()

    with open('INFO.md', 'r') as info:
        infopage = Page('Info', info.read().decode('utf-8'))
        persist(infopage)
