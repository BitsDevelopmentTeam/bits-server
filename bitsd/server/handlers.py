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
import tornado.auth

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


class LoginPageHandler(BaseHandler, tornado.auth.GoogleMixin):
    """Handle login browser requests for reserved area."""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """Display the login page."""
        if self.get_argument("openid.mode", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie("usertoken", user['claimed_id'],
                                   expires_days=1)
            self.redirect(self.get_argument('next', default='/'))
        else:
            self.authenticate_redirect()


class LogoutPageHandler(BaseHandler):
    """Handle login browser requests for logout from reserved area."""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        """Display the logout page."""
        self.clear_cookie("usertoken")
        self.write("Logged out.")


class AdminPageHandler(BaseHandler):
    """Handle browser requests for admin area."""

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        """Display the admin page."""
        self.render('templates/admin.html',
                    page_message='Very secret information here')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def post(self):
        """Issue admin commands."""
        status = self.get_argument('changestatus', default=None)
        if status: self.submit_status(status)

    def submit_status(self, status):
        """Submit maually a new status to the BITS system"""

        #To prevent from saving random stuff in the db
        #coming form the status variable
        textstatus = 'open' if (status == 'open') else 'closed'

        curstatus = query.get_current_status()
        if curstatus is None or curstatus.value != textstatus:
            LOG.info('Change of BITS status to status={}'.format(textstatus) +
                     ' from web interface.')
            status = query.log_status(textstatus, 'BITS')
            broadcast(status.jsondict(wrap=True)) # wrapped in a dict
            message = "Modifica dello stato effettuata."
        else:
            message = "Stato gia' aperto/chiuso! Ignoro."
            LOG.error('BITS already open/closed! Ignoring.')
        
        self.render('templates/admin.html', page_message = message)


    def get_login_url(self):
        """Returns the login URL if the client is not logged"""
        return '/login'

    def get_current_user(self):
        """Returns the current user as seen from the signed cookie"""
        return self.get_secure_cookie('usertoken')


