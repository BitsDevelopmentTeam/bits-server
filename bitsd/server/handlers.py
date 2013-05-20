#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
HTTP requests handlers.
"""

import markdown
import datetime

import tornado.web
import tornado.websocket

from tornado.options import options

from .notifier import MessageNotifier

import bitsd.persistence.query as query

from bitsd.common import LOG


def cache(seconds):
    """
    Caching decorator for handlers. Will set `Expires` and `Cache-Control`
    headers appropriately.

    Example: to cache resource for 10 days, use::

        class FooHandler(BaseHandler):
            @cache(3600 * 24 * 10)
            def get(self):
                return render_something_great()

    Parameters:
        `seconds`: TTL of the cached resource, in seconds.
    """
    def set_cacheable(get_function):
        def wrapper(self, *args, **kwargs):
            self.set_header("Expires", datetime.datetime.utcnow() +
                datetime.timedelta(seconds=seconds))
            self.set_header("Cache-Control", "max-age=" + str(seconds))
            return get_function(self, *args, **kwargs)
        return wrapper
    return set_cacheable


def broadcast(message):
    """Broadcast given message to all clients. `message`
    may be either a string, which is directly broadcasted, or a dictionay
    that is JSON-serialized automagically before sending."""
    StatusHandler.CLIENTS.broadcast(message)


class BaseHandler(tornado.web.RequestHandler):
    """Base requests handler"""
    pass


class HomePageHandler(BaseHandler):
    """Display homepage."""
    @cache(86400*10)
    def get(self):
        self.render('templates/homepage.html')


class DataPageHandler(BaseHandler):
    """Get BITS data in JSON, machine parseable."""
    def get(self):
        self.write(query.get_latest_data())
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
            latest_statuses=query.get_latest_statuses(
                offset=offset,
                limit=self.LINES_PER_PAGE
            ),
            # Used by the paginator
            offset=offset,
            limit=self.LINES_PER_PAGE,
            count=query.get_number_of_statuses(),
        )


class StatusPageHandler(BaseHandler):
    """Get a single digit, indicating BITS status (open/closed)"""
    def get(self):
        status = query.get_current_status()
        self.write('1' if status is not None and status.value == 'open' else '0')
        self.finish()


class MarkdownPageHandler(BaseHandler):
    """Renders page from markdown source."""
    def get(self, slug):
        page = query.get_page(slug)

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
        self.write_message(query.get_latest_data())
        LOG.debug('Registered client')

    def on_message(self, message):
        """Disconnect clients sending data (they should not)."""
        LOG.warning('Client sent a message: disconnected.')

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.CLIENTS.unregister(self)
        LOG.debug('Unregistered client.')

