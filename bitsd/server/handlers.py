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
import json
import re
import hashlib
import hmac

import markdown
from datetime import datetime, timedelta
from sqlalchemy import distinct
from sqlalchemy.exc import IntegrityError

from tornado.web import MissingArgumentError, HTTPError, RequestHandler
import tornado.websocket
import tornado.auth

from tornado.options import options

import bitsd.listener.notifier as notifier
from bitsd.persistence.engine import session_scope, persist
from bitsd.persistence.models import Status, User, MACToUser, LoginAttempt

from .auth import verify, DoSError
from .presence import PresenceForecaster
from .notifier import MessageNotifier

import bitsd.persistence.query as query

from bitsd.common import LOG, secure_compare


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
            self.set_header("Expires", datetime.utcnow() +
                timedelta(seconds=seconds))
            self.set_header("Cache-Control", "max-age=" + str(seconds))
            return get_function(self, *args, **kwargs)
        return wrapper
    return set_cacheable


def broadcast(message):
    """Broadcast given message to all clients. `message`
    may be either a string, which is directly broadcasted, or a dictionay
    that is JSON-serialized automagically before sending."""
    StatusHandler.CLIENTS.broadcast(message)


class BaseHandler(RequestHandler):
    """Base requests handler"""
    USER_COOKIE_NAME = "usertoken"

    def get_current_user(self):
        """Retrieve current user name from secure cookie."""
        return self.get_secure_cookie(
            self.USER_COOKIE_NAME,
            max_age_days=options.cookie_max_age_days
        )

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

    def get(self):
        """Display and paginate log."""
        wants_json = self.get_argument("format", "html") == "json"
        offset = self.get_integer_or_400("offset", 0)
        limit = self.get_integer_or_400("limit", self.LINES_PER_PAGE)

        with session_scope() as session:
            latest_statuses = query.get_latest_statuses(
                session,
                offset=offset,
                limit=limit
            )

            # Handle limit = 1 case (result is not a list)
            if type(latest_statuses) == Status:
                latest_statuses = [latest_statuses]

            if wants_json:
                self.write(self.jsonize(latest_statuses))
                self.finish()
            else:
                self.render('templates/log.html',
                    latest_statuses=latest_statuses,
                    # Used by the paginator
                    offset=offset,
                    limit=self.LINES_PER_PAGE,
                    count=query.get_number_of_statuses(session),
                )

    @staticmethod
    def jsonize(latest_statuses):
        """Turn an array of Status objects into a JSON-serializable dict"""
        data = [s.jsondict(wrap=False) for s in latest_statuses]
        return {"log": data}

    def get_integer_or_400(self, name, default):
        """Try to get the parameter by name (and default), then convert it to
        integer. In case of failure, raise a HTTP error 400"""
        try:
            return int(self.get_argument(name, default))
        except ValueError:
            raise tornado.web.HTTPError(400)


class StatusPageHandler(BaseHandler):
    """Get a single digit, indicating BITS status (open/closed)"""
    def get(self):
        with session_scope() as session:
            status = query.get_current_status(session)
            answer = '1' if status is not None and status.value == Status.OPEN else '0'
        self.write(answer)
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

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.CLIENTS.unregister(self)
        LOG.debug('Unregistered client.')
        
    def check_origin(self, origin):
        """No Same-Origin Policy"""
        return True


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
                message=None,
                show_recaptcha=False
            )

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        ip_address = self.request.remote_ip
        next = self.get_argument("next", "/")
        captcha_challenge = self.get_argument("recaptcha_challenge_field", "")
        captcha_response = self.get_argument("recaptcha_response_field", "")
        has_recaptcha = captcha_challenge or captcha_response

        with session_scope() as session:
            try:
                verified = verify(session, username, password, ip_address, has_recaptcha, captcha_challenge, captcha_response)
            except DoSError as error:
                LOG.warning("DoS protection: %s", error)
                self.log_offender_details()
                self.render(
                    'templates/login.html',
                    next=next,
                    message="Tentativi dal tuo IP over 9000...",
                    show_recaptcha=True,
                    previous_attempt_incorrect=has_recaptcha
                )
                return

        if verified:
            self.set_secure_cookie(
                self.USER_COOKIE_NAME,
                username,
                expires_days=options.cookie_max_age_days
            )
            LOG.info("Authenticating user %r", username)
            self.redirect(next)
        else:
            LOG.warning("Failed authentication for user %r", username)
            self.log_offender_details()
            self.render(
                'templates/login.html',
                next=next,
                message="Password/username sbagliati!",
                show_recaptcha=has_recaptcha,
                # If we have a captcha at this point, it means we already failed once
                previous_attempt_incorrect=True
            )

    def log_offender_details(self):
        userAgent = self.request.headers.get("User-Agent", '<unknown>')
        remoteIp = self.request.remote_ip
        LOG.warning("Request came from %s, user agent is '%s'", remoteIp, userAgent)


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
        self.render(
            'templates/admin.html',
            page_message='Very secret information here',
            roster=MACUpdateHandler.ROSTER
        )

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

            LOG.info('Change of BITS to status=%r from web interface.', textstatus)
            message = ''
            try:
                status = query.log_status(session, textstatus, 'web')
                broadcast(status.jsondict())
                notifier.send_status(textstatus)
                message = "Ora la sede è {}.".format(textstatus)
            except IntegrityError:
                LOG.error("Status changed too quickly, not logged.")
                message = "Errore: modifica troppo veloce!"
                raise
            finally:
                self.render(
                    'templates/admin.html',
                    page_message=message,
                    roster=MACUpdateHandler.ROSTER
                )


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


class MessagePageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('templates/message.html', message=None, text='')

    @tornado.web.authenticated
    def post(self):
        text = self.get_argument('msgtext')
        username = self.get_current_user()

        LOG.info("%r sent message %r from web", username, text)

        with session_scope() as session:
            user = query.get_user(session, username)
            message = query.log_message(session, user, text)
            LOG.info("Broadcasting to clients")
            broadcast(message.jsondict())
            LOG.info("Notifying Fonera")
            notifier.send_message(text)

        self.render(
            'templates/message.html',
            message='Messaggio inviato correttamente!',
            text=text
        )


class MACPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('templates/submitmac.html', message=None, text='')

    @tornado.web.authenticated
    def post(self):
        mac = self.get_argument('msgtext').lower()
        if not re.match("((?:[a-f0-9]{2}:){5}[a-f0-9]{2})", mac):
            self.render(
                'templates/submitmac.html',
                message='MAC address non valido.',
                text=mac
            )           
            return

        username = self.get_current_user()

        LOG.info("%r requested to add a new MAC address", username)

        with session_scope() as session:
            user = query.get_user(session, username)
            mac_hash = hmac.new(options.mac_hash_salt, mac,
                                hashlib.sha256).hexdigest()
            if query.get_userid_from_mac_hash(session, mac_hash) != None:
                message = u'Il MAC address è già presente nel database.'
            else:
                query.log_user_mac(session, user, mac_hash)
                message = 'MAC address associato al tuo utente.'
           
        self.render(
            'templates/submitmac.html',
            message=message,
            text=''
        )


class RTCHandler(BaseHandler):
    def get(self):
        now = datetime.now()
        self.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        self.finish()


class MACUpdateHandler(BaseHandler):
    ROSTER = []

    def post(self):
        now = datetime.now()
        remote_ip = self.request.remote_ip

        with session_scope() as session:
            last = query.get_last_login_attempt(session, remote_ip)
            if last is None:
                last = LoginAttempt(None, remote_ip)
                persist(session, last)
            else:
                if (now - last.timestamp) < timedelta(seconds=options.mac_update_interval):
                    LOG.warning("Too frequent attempts to update, remote IP address is %s", remote_ip)
                    raise HTTPError(403, "Too frequent")
                else:
                    last.timestamp = now
                    persist(session, last)

        try:
            password = self.get_argument("password")
            macs = self.get_argument("macs")
        except MissingArgumentError:
            LOG.warning("MAC update received malformed parameters: %s", self.request.arguments)
            raise HTTPError(400, "Bad parameters list")

        if not secure_compare(password, options.mac_update_password):
            LOG.warning("Client provided wrong password for MAC update!")
            raise HTTPError(403, "Wrong password")

        LOG.info("Authorized request to update list of checked-in users from IP address %s", remote_ip)

        macs = json.loads(macs)

        with session_scope() as session:
            names = session.\
                query(distinct(User.name)).\
                filter(User.userid == MACToUser.userid).\
                filter(MACToUser.mac_hash .in_ (macs)).\
                all()

        MACUpdateHandler.ROSTER = [n[0] for n in names]
        LOG.debug("Updated list of checked in users: %s", MACUpdateHandler.ROSTER)

    def check_xsrf_cookie(self):
        # Since this is an API call, we need to disable anti-XSRF protection
        pass
