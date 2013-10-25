# -*- coding: utf-8 -*-
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
from sqlalchemy.exc import IntegrityError

import tornado.web
import tornado.websocket
import tornado.auth

from tornado.options import options
from bitsd.persistence.engine import session_scope
from bitsd.persistence.models import Status

from .auth import verify
from bitsd.server.presence import PresenceForecaster
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
    USER_COOKIE_NAME = "usertoken"

    def get_current_user(self):
        """Retrieve current user name from secure cookie."""
        return self.get_secure_cookie(
            self.USER_COOKIE_NAME,
            max_age_days=options.cookie_max_age_days
        )

    def get_current_user_entity(self):
        """Retrieve current user entity from DB."""
        with session_scope() as session:
            username = self.get_current_user()
            return query.get_user(session, username) if username else None

    def get_login_url(self):
        return '/login'


class HomePageHandler(BaseHandler):
    """Display homepage."""
    @cache(86400*10)
    def get(self):
        self.render('templates/homepage.html')


class DataPageHandler(BaseHandler):
    """Get BITS data in JSON, machine parseable."""
    def get(self):
        with session_scope() as session:
            self.write(query.get_latest_data(session))
        self.finish()


class LogPageHandler(BaseHandler):
    """Handle historical data browser requests."""
    LINES_PER_PAGE = 20

    @tornado.web.removeslash
    def get(self, offset):
        """Display and paginate log."""

        # We can safely cast to int() because of the path regex \d+
        offset = int(offset) if offset is not None else 0

        with session_scope() as session:
            self.render('templates/log.html',
                latest_statuses=query.get_latest_statuses(
                    session,
                    offset=offset,
                    limit=self.LINES_PER_PAGE
                ),
                # Used by the paginator
                offset=offset,
                limit=self.LINES_PER_PAGE,
                count=query.get_number_of_statuses(session),
            )


class StatusPageHandler(BaseHandler):
    """Get a single digit, indicating BITS status (open/closed)"""
    def get(self):
        with session_scope() as session:
            status = query.get_current_status(session)
        self.write('1' if status is not None and status.value == Status.OPEN else '0')
        self.finish()


class MarkdownPageHandler(BaseHandler):
    """Renders page from markdown source."""
    @cache(86400*10)
    def get(self, slug):
        with session_scope() as session:
            page = query.get_page(session, slug)

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
        with session_scope() as session:
            latest = query.get_latest_data(session)
        self.write_message(latest)
        LOG.debug('Registered client')

    def on_message(self, message):
        """Disconnect clients sending data (they should not)."""
        LOG.warning('Client sent a message: disconnected.')

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.CLIENTS.unregister(self)
        LOG.debug('Unregistered client.')


class LoginPageHandler(BaseHandler):
    """Handle login browser requests for reserved area."""
    def get(self):
        next = self.get_argument("next", "/")
        if self.get_current_user():
            self.redirect(next)
        else:
            self.render(
                'templates/login.html',
                next=next,
                message=None
            )

    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        next = self.get_argument("next", "/")

        with session_scope() as session:
            authenticated = verify(session, username, password)

        if authenticated:
            self.set_secure_cookie(
                self.USER_COOKIE_NAME,
                username,
                expires_days=options.cookie_max_age_days
            )
            LOG.info("Authenticating user `{}`".format(username))
            self.redirect(next)
        else:
            LOG.warning("Wrong authentication for user `{}`".format(username))
            self.render(
                'templates/login.html',
                next=next,
                message="Password/username sbagliati!"
            )


class LogoutPageHandler(BaseHandler):
    """Handle login browser requests for logout from reserved area."""

    def get(self):
        """Display the logout page."""
        self.clear_cookie("usertoken")
        self.redirect("/")


class AdminPageHandler(BaseHandler):
    """Handle browser requests for admin area."""

    @tornado.web.authenticated
    def get(self):
        """Display the admin page."""
        self.render('templates/admin.html',
                    page_message='Very secret information here')

    @tornado.web.authenticated
    def post(self):
        """Issue admin commands."""
        status = self.get_argument('changestatus', default=None)
        if status: self.change_status()

    def change_status(self):
        """Manually change the status of the BITS system"""

        with session_scope() as session:
            curstatus = query.get_current_status(session)

            if curstatus is None:
                textstatus = Status.CLOSED
            else:
                textstatus = Status.OPEN if curstatus.value == Status.CLOSED else Status.CLOSED

            LOG.info('Change of BITS to status={}'.format(textstatus) +
                     ' from web interface.')
            message = ''
            try:
                status = query.log_status(session, textstatus, 'web')
                broadcast(status.jsondict())
                message = "Ora la sede è {}.".format(textstatus)
            except IntegrityError:
                LOG.error("Status changed too quickly, not logged.")
                message = "Errore: modifica troppo veloce!"
                raise
            finally:
                self.render('templates/admin.html', page_message=message)


class PresenceForecastHandler(BaseHandler):
    """Handler for presence stats.
    Upon GET, it will render JSON-encoded probabilities,
    as a 2D array (forecast for each weekday, at 30min granularity)."""
    FORECASTER = PresenceForecaster()

    @cache(86400)
    def get(self):
        data = self.FORECASTER.forecast()
        self.write({"forecast": data})
        self.finish()
