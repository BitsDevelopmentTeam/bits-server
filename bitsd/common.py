#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""Common elements needed by all modules."""

from tornado.netutil import bind_sockets, bind_unix_socket

import logging


#: Main logger
LOG = logging.getLogger('tornado.general')


def bind(server, port, usocket):
    """Make server listen on port (inet socket).
    If given, prefer `usocket`, path to a unix socket.
    The latter is useful for reverse proxying"""

    # If we have a unix socket path
    if usocket:
        LOG.info('Starting on unix socket `{}`'.format(usocket))
        try:
            socket = bind_unix_socket(usocket)
        except OSError as e:
            LOG.error('Cannot create unix socket: {}'.format(e))
        else:
            server.add_socket(socket)
            LOG.info('Started')
    else:
        LOG.info('Starting on port {}'.format(port))
        sockets = bind_sockets(port)
        server.add_sockets(sockets)
        LOG.info('Started')
