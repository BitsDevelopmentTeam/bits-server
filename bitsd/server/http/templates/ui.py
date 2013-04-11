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

from bitsd.persistence.logger import get_latest_statuses


class BasePage(tornado.web.UIModule):
    """Module providing base css, ico files for all pages and encoding tag."""
    def css_files(self):
        css = ['/static/default.css?v=1',]
        # FIXME daltonism workaround, should be implemented client-side
        if 'blind' in self.request.path:
            css.append('/static/dalton.css?v=1')
        return css

    def html_head(self):
        return  """
<meta charset="utf-8"/>
<link rel="icon" href="/static/open.ico" id="favicon"/>
        """

    def render(self):
        return ''


class DynamicPage(tornado.web.UIModule):
    """Module providing JS for dynamic pages."""
    def javascript_files(self):
        return (
            '/static/raphael-min.js?v=1',
            '/static/g.raphael-min.js?v=1',
            '/static/g.line-min.js?v=1',
            '/static/json2.js?v=1',
            '/static/module.js?v=1',
            '/static/debug.js?v=1',
            '/static/html5.js?v=1',
            '/static/peppy.js?v=1',
            '/static/browser_handler.js?v=1',
            '/static/handler.js?v=1',
            '/static/websocket.js?v=1',
            '/static/index_main.js?v=1',
        )

    def render(self):
        return ''


class PresenceWidget(tornado.web.UIModule):
    """Render a table showing the probability to find the BITS open,
    visualized as shades of colour, from green to red."""
    def css_files(self):
        return ()

    def render(self):
        samples = get_latest_statuses(5000)
        #TODO + TODO gray
        return '<img src="bits_presence.png" alt="Grafico delle presenze" id="presence_graph"/>'
