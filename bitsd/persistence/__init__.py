#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Actual DBMS proxy.
"""

from bitsd.common import LOG
from . import models, engine


def start():
    """Will setup connection and ensure that all tables exist.
    MUST be called prior to any operation."""
    LOG.info('Connecting to DB...')
    engine.connect()

    # Create tables if they don't exist.
    LOG.info('Checking tables in the DB...')
    models.check()

    LOG.info('Done')

