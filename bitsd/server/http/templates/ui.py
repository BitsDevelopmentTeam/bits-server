#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Assorted Tornado UI widgets and mixins.
"""

import tornado.web


class BasePage(tornado.web.UIModule):
    """Module providing base css, ico files for all pages and encoding tag."""
    #TODO daltonic?
    def css_files(self):
        return ('/css/default.css',)

    def html_head(self):
        return  """
<meta charset="utf-8"/>
<link rel="icon" href="/img/open.ico" id="favicon"/>
        """

    def render(self):
        return ''


class DynamicPage(tornado.web.UIModule):
    """Module providing JS for dynamic pages."""
    def javascript_files(self):
        return (
            '/js/raphael-min.js',
            '/js/g.raphael-min.js',
            '/js/g.line-min.js',
            '/js/json2.js',
            '/js/module.js',
            '/js/debug.js',
            '/js/html5.js',
            '/js/peppy.js',
            '/js/browser_handler.js',
            '/js/handler.js',
            '/js/websocket.js',
            '/js/index_main.js',
        )

    def render(self):
        return ''
