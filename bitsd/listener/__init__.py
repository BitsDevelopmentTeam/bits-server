#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Listeners are server components waiting for commands on given
ports/hosts/address or events (on the countrary, a server will actually
*serve* content to the client).
"""


from tornado.options import options

from .handlers import RemoteListener
from bitsd.common import bind, LOG

def start():
    """Connect and bind listeners. **MUST** be called at startup."""
    fonera = RemoteListener()
    LOG.info('Starting remote control...')
    LOG.info(
        'My IP is {}, remote IP is {}'.format(
            options.control_local_address,
            options.control_remote_address
        )
    )
    bind(
        fonera,
        options.control_local_port,
        options.control_local_usocket,
        address=options.control_local_address
    )
