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
import tornado.websocket

from tornado.options import options

from .notifier import MessageNotifier

from bitsd.persistence.logger import get_latest_statuses, get_number_of_statuses
from bitsd.persistence.logger import get_current_status
from bitsd.persistence.pages import get_page

import bitsd.persistence.logger as logger
import bitsd.persistence.message as message

from bitsd.common import LOG


class BaseHandler(tornado.web.RequestHandler):
    """Base requests handler"""
    pass


class HomePageHandler(BaseHandler):
    """Display homepage."""
    def get(self):
        self.render('templates/homepage.html')


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

        self.render('templates/log.html',
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

        self.render('templates/mdpage.html',
            body=markdown.markdown(
                page.body,
                safe_mode='escape' if options.mdescape else False,
            ),
            title=page.title,
        )


class StatusHandler(tornado.websocket.WebSocketHandler):
    """Handler for POuL status via websocket"""

    CLIENTS = MessageNotifier('Status handler queue')

    def open(self):
        """Register new handler with MessageNotifier."""
        StatusHandler.CLIENTS.register(self)
        self.write_message(get_latest_data())
        LOG.debug('Registered client')

    def on_message(self, message):
        """Disconnect clients sending data (they should not)."""
        LOG.warning('Client sent a message: disconnected.')

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.CLIENTS.unregister(self)
        LOG.debug('Unregistered client.')


def get_latest_data():
    """Get recent data."""
    status = logger.get_current_status()
    temp = logger.get_current_temperature()
    latest_temp_samples = logger.get_latest_temperature_samples()
    latest_message = message.get_current_message()

    json_or_none = lambda data: data.jsondict() if data is not None else ""
    return {
        "status": json_or_none(status),
        "tempint": json_or_none(temp),
        "version": options.jsonver,
        "msg": json_or_none(latest_message),
        "tempinthist": [sample.jsondict() for sample in latest_temp_samples]
    }
