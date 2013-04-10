#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web
import markdown

from bitsd.persistence.pages import get_page

class MarkdownPageHandler(tornado.web.RequestHandler):
    """Renders page from markdown source."""
    def get(self, slug):
        page = get_page(slug)

        self.render('markdown.html',
            body=markdown.markdown(
                page.body,
                safe_mode='escape',
            ),
            title=page.title,
        )
