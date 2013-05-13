#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Listen for remote commands on BITS-miniprotocol and dispatches to Fonera
via bitsd.client.fonera.Fonera proxy.
"""

from tornado.options import options

from .handler import RemoteListener
from bitsd.common import bind, LOG

def start():
    """Connect and bind listeners. **MUST** be called at startup."""
    fonera = RemoteListener()
    LOG.info('Starting remote control...')
    LOG.info('Remote control IP is {}'.format(options.remote_address))
    bind(fonera, options.remote_port, options.remote_usocket,
        address=options.remote_address)
