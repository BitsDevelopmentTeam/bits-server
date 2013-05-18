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
import tornado.httpserver

from tornado.options import options

from . import handlers
from . import uimodules

from bitsd.common import LOG, bind


def start():
    """Setup HTTP server. **MUST** be called prior to any operation."""
    application = tornado.web.Application([
            # FIXME daltonism workaround, should be implemented client-side
            (r'/(?:|blind)', handlers.HomePageHandler),
            (r'/log(?:/?|/(\d+))', handlers.LogPageHandler),
            (r'/status', handlers.StatusPageHandler),
            (r'/data', handlers.DataPageHandler),
            (r'/(info)', handlers.MarkdownPageHandler),
        ],
        ui_modules=uimodules,
        gzip=True,
        debug=options.developer_mode,
        static_path=options.assets_path,
        xsrf_cookies=True,
        cookie_secret=options.cookie_secret
    )

    server = tornado.httpserver.HTTPServer(application) #TODO other options
    LOG.info('Starting HTTP server...')
    bind(server, options.web_port, options.web_usocket)
