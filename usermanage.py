#! /usr/bin/env python
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Add, remove and modify users in database
"""

# DO NOT REMOVE
import bitsd.properties

from bitsd.persistence.engine import session_scope
from bitsd.persistence import start
from bitsd.server.auth import useradd, userdel, usermod
from tornado.options import parse_config_file


import sys
from getpass import getpass


if __name__ == '__main__':
    try:
        parse_config_file('/etc/bitsd.conf')
    except IOError:
        print ("[INFO] No /etc/bitsd.conf found, ignoring.")

    action = sys.argv[1]
    username = sys.argv[2]

    start()

    with session_scope() as session:
        if action == 'add':
            password = getpass('Password for `{}`:'.format(username))
            useradd(session, username, password)
        elif action == 'delete':
            userdel(session, username)
        elif action == 'modify':
            password = getpass('New password for `{}`:'.format(username))
            usermod(session, username, password)
