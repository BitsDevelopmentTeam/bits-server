#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web
from tornado.options import options

from .status import StatusHandler

from bitsd.common import LOG

def startserver():
    LOG.debug('Starting websocket server on port {}'.format(options.web_port))
    server = tornado.web.Application([
        (r'/', StatusHandler)
    ])
    server.listen(options.ws_port)
