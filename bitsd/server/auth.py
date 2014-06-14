#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#
from datetime import datetime, timedelta

from passlib.hash import sha512_crypt as Hasher
from tornado.options import options
from recaptcha import RecaptchaClient

from bitsd.persistence.query import get_user, get_last_login_attempt, log_last_login_attempt
from bitsd.persistence.models import User
from bitsd.persistence.engine import persist, delete

from bitsd.common import LOG


class ReCaptcha(object):
    is_solution_correct = None
    get_challenge_markup = None

    @classmethod
    def init(cls):
        """"Lazily create reCAPTCHA object. This MUST be called before using ReCaptcha.

        Lazy init allows to load keys from config file."""
        client = RecaptchaClient(options.recaptcha_privkey, options.recaptcha_pubkey, recaptcha_options={"theme": "white"})
        cls.is_solution_correct = client.is_solution_correct
        cls.get_challenge_markup = client.get_challenge_markup


class DoSError(Exception):
    """DoS error: raise by verify() if the user is trying
    to authenticate too fast"""
    pass


def verify(session, username, supplied_password, ip_address, has_captcha, recaptcha_challenge, recaptcha_response):
    """Verify user credentials.

    If the username exists, then the supplied password is hashed and
    compared with the stored hash. Otherwise, an hash is calculated and discarded.

    An hash is calculated regardless of the existence of the username, so that
    the response time is approximately the same whether the username exists or not,
    mitigating a timing attack to reveal valid usernames.

    In order to mitigate DoS/bruteforce attacks, two temporal limitations are enforced:

    1. Max 1 failed login attempt per IP address each second (regardless of username)
    2. Max 1 failed login attempt per each username per IP address each
       `min_log_retry` seconds (see bitsd.properties), whether the username
       exists or not.

    A DoS protection is necessary because password hashing is an expensive operation.
    """
    if has_captcha:
        solved_captcha = ReCaptcha.is_solution_correct(recaptcha_response, recaptcha_challenge, ip_address)
        # Exit immediately if wrong answer
        if not solved_captcha:
            return False
    else:
        solved_captcha = False

    # Save "now" so that the two timestamp checks are referred to the same instant
    now = datetime.now()

    def detect_dos(attempt, timeout):
        if solved_captcha:
            return False

        # Otherwise, check timing
        if attempt is not None:
            too_quick = (now - attempt.timestamp) < timeout
            if too_quick:
                log_last_login_attempt(session, ip_address, username)
                return True
            else:
                # Clean up if no more relevant
                session.delete(attempt)
        return False

    last_attempt_for_ip = get_last_login_attempt(session, ip_address)
    last_attempt_for_ip_and_username = get_last_login_attempt(session, ip_address, username)

    if detect_dos(last_attempt_for_ip, timedelta(seconds=1)):
        raise DoSError("Too frequent requests from {}".format(ip_address))

    if detect_dos(last_attempt_for_ip_and_username, timedelta(seconds=options.min_login_retry)):
        raise DoSError("Too frequent attempts from {} for username `{}`".format(ip_address, username))

    user = get_user(session, username)

    if user is None:
        LOG.warn("Failed attempt for non existent user `{}`".format(username))
        # Calculate hash anyway (see docs for the explanation)
        Hasher.encrypt(supplied_password)
        log_last_login_attempt(session, ip_address, username)
        return False
    else:
        valid = Hasher.verify(supplied_password, user.password)
        if not valid:
            log_last_login_attempt(session, ip_address, username)
        return valid


def useradd(session, username, password):
    """Add user with hashed password to database"""
    user = User(username, Hasher.encrypt(password))
    persist(session, user)


def userdel(session, username):
    """Delete user from database."""
    user = get_user(session, username)
    delete(session, user)


def usermod(session, username, password):
    """"Modify password for existing user."""
    user = get_user(session, username)
    user.password = Hasher.encrypt(password)
    persist(session, user)
