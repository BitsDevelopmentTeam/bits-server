#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web
from tornado.options import options

from .homepage import HomePageHandler
from .log import LogPageHandler
from .data import DataPageHandler

from bitsd.common import LOG

def startserver():
    LOG.debug('Starting web server on port {}'.format(options.web_port))
    server = tornado.web.Application([
            (r'/', HomePageHandler),
            (r'/storico', LogPageHandler),
            (r'/data.json', DataPageHandler),
        ],
    )
    server.listen(options.web_port)