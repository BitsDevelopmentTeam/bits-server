#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
HTTP pages handlers
"""

import markdown
import tornado.web
from tornado.options import options

from .. import get_latest_data

from bitsd.persistence.logger import get_latest_statuses, get_number_of_statuses
from bitsd.persistence.logger import get_current_status
from bitsd.persistence.pages import get_page


class BaseHandler(tornado.web.RequestHandler):
    """Base requests handler"""
    pass


class HomePageHandler(BaseHandler):
    """Display homepage."""
    def get(self):
        self.render('homepage.html')


class DataPageHandler(BaseHandler):
    """Get BITS data in JSON, machine parseable."""
    def get(self):
        self.write(get_latest_data())
        self.finish()


class LogPageHandler(BaseHandler):
    """Handle historical data browser requests."""
    LINES_PER_PAGE = 20

    @tornado.web.removeslash
    def get(self, offset):
        """Display and paginate log."""

        # We can safely cast to int() because of the path regex \d+
        offset = int(offset) if offset is not None else 0

        self.render('log.html',
            latest_statuses=get_latest_statuses(
                offset=offset,
                limit=self.LINES_PER_PAGE
            ),
            # Used by the paginator
            offset=offset,
            limit=self.LINES_PER_PAGE,
            count=get_number_of_statuses(),
        )


class StatusPageHandler(BaseHandler):
    """Get a single digit, indicating BITS status (open/closed)"""
    def get(self):
        status = get_current_status()
        self.write('1' if status is not None and status.value == 'open' else '0')
        self.finish()


class MarkdownPageHandler(BaseHandler):
    """Renders page from markdown source."""
    def get(self, slug):
        page = get_page(slug)

        if page is None:
            raise tornado.web.HTTPError(404)

        self.render('mdpage.html',
            body=markdown.markdown(
                page.body,
                safe_mode='escape' if options.mdescape else False,
            ),
            title=page.title,
        )
