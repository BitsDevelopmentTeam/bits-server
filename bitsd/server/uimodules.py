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
from tornado.options import options


class DebugMode(tornado.web.UIModule):
    """If in developer mode, then render a debug meta header
    which will toggle verbose JS logging."""
    def render(self):
        return '<meta name="mode" content="debug"/>' if options.developer_mode else ''


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
            '/static/lib/zepto.min.js?v=1.0',
            '/static/lib/Chart.min.js?v=0.2',
        )

    def html_body(self):
        return "<script src='/static/lib/require.js?v=2.1.9' data-main='/static/" + self._main + "' type='text/javascript'></script>"

    def render(self, main = "other"):
        self._main = main
        return ''


class PresenceWidget(tornado.web.UIModule):
    """Render a table showing the probability to find the BITS open,
    visualized as shades of colour, from green to red."""
    def css_files(self):
        return ()

    def render(self):
        #TODO samples = get_latest_statuses(5000)
        #TODO + TODO gray
        return '<img src="bits_presence.png" height=380 width=380 alt="Grafico delle presenze" id="presence_graph"/>'


class PaginatorWidget(tornado.web.UIModule):
    """Render a page browser, with Back/Forward links.
    Navigation links are created by appending `/n` to the `baseurl`, where `n`
    is a calculated the offset from the first element of the paginated list.

    Parameters:
        `baseurl`: the url used as a base to pagination links (see above).
        `offset`: first element to show, counting from the first of the paginated list
        `limit`: number of elements to show in each page.
        `count`: total number of elements to paginate.

    Returns:
        None
    """
    def render(self, baseurl, offset, limit, count):
        return self.render_string('templates/paginator.html',
            baseurl=baseurl,
            offset=offset,
            limit=limit,
            count=count
        )
