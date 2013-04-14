#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Websockets server.
"""

import tornado.web
import tornado.httpserver

from tornado.options import options

from .status import StatusHandler

from bitsd.common import LOG
from bitsd.server import bind


def start():
    application = tornado.web.Application([
        (r'/', StatusHandler)
    ])

    server = tornado.httpserver.HTTPServer(application)
    LOG.info('Starting websocket server...')
    bind(server, options.ws_port, options.ws_usocket)
