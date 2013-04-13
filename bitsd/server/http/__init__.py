#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
HTTP content server
"""

import tornado.web
from tornado.options import options

from .homepage import HomePageHandler
from .log import LogPageHandler
from .data import DataPageHandler
from .status import StatusPageHandler
from .mdpage import MarkdownPageHandler
from .templates import ui

from bitsd.common import LOG

def start():
    LOG.debug('Starting web server on port {}'.format(options.web_port))
    server = tornado.web.Application([
            # FIXME daltonism workaround, should be implemented client-side
            (r'/(?:|blind)', HomePageHandler),
            (r'/log(?:/?|/(\d+))', LogPageHandler),
            (r'/status', StatusPageHandler),
            (r'/data', DataPageHandler),
            (r'/(info)', MarkdownPageHandler),
        ],
        ui_modules=ui,
        gzip=True,
        debug=options.developer_mode,
        static_path=options.assets_path
    )
    server.listen(options.web_port)
