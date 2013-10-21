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

from bitsd.persistence import start
from bitsd.server.auth import useradd, userdel, usermod
from tornado.options import parse_config_file

from sqlalchemy.exc import IntegrityError

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

    if action == 'add':
        password = getpass('Password for `{}`:'.format(username))
        try:
            useradd(username, password)
        except IntegrityError:
            print "Error: user is already in database!"
    elif action == 'delete':
        userdel(username)
    elif action == 'modify':
        password = getpass('New password for `{}`:'.format(username))
        usermod(username, password)
