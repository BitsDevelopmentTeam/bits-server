#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""Common elements needed by all modules."""

from tornado.netutil import bind_sockets, bind_unix_socket
from tornado.options import options

import logging
import os


#: Main logger
LOG = logging.getLogger('tornado.general')


def bind(server, port, usocket, address=None, mode=None):
    """Make server listen on port (inet socket).
    If given, prefer `usocket`, path to a unix socket.
    The latter is useful for reverse proxying.

    If listening on a inet socket, `address` might be
    given. `address` may be either an IP address or hostname.
    If it's a hostname, the server will listen on all IP addresses
    associated with the name. If not given (and not listening on a unix
    socket) will listen on all available interfaces."""

    # If we have a unix socket path
    if usocket:
        LOG.info('Starting on unix socket `{}`'.format(usocket))
        try:
            socket = bind_unix_socket(usocket, mode)
            os.chown(usocket, options.usocket_uid, options.usocket_gid)
        except OSError as error:
            LOG.error('Cannot create unix socket: {}'.format(error))
        else:
            server.add_socket(socket)
            LOG.info('Started')
    else:
        LOG.info('Starting on port {}'.format(port))
        sockets = bind_sockets(port, address=address)
        server.add_sockets(sockets)
        LOG.info('Started')
