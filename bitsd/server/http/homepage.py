#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web

class HomePageHandler(tornado.web.RequestHandler):
    """Display homepage."""
    JS = [
        'js/raphael-min.js',
        'js/g.raphael-min.js',
        'js/g.line-min.js',
        'js/json2.js',
        'js/module.js',
        'js/debug.js',
        'js/html5.js',
        'js/peppy.js',
        'js/browser_handler.js',
        'js/handler.js',
        'js/websocket.js',
        'js/index_main.js',
    ]

    def get(self):
        self.render('homepage.html',
            javascripts=self.JS
        )
