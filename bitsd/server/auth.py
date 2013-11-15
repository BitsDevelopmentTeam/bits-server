#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#
from datetime import datetime

from passlib.hash import sha512_crypt as Hasher
from tornado.options import options
from bitsd.persistence.query import get_user
from bitsd.persistence.models import User
from bitsd.persistence.engine import persist, delete
from bitsd.common import LOG


class DoSError(Exception):
    """DoS error: raise by verify() if the user is trying
    to authenticated too fast"""
    def __init__(self, timeSinceLastAttempt):
        Exception.__init__(self, "Login attempt is too fast!")
        self.timeSinceLastAttempt = timeSinceLastAttempt


def verify(session, username, suppliedPassword):
    """Try to verify the user in a smart way.
    In fact, password hash will be calculated only if the username
    exists in the DB and if at least `min_login_retry` (see bitsd.properties)
    seconds have passed since last login attempt (mitigating a possible DoS).

    In case of fast tries, a DoSError exception will be raised"""
    user = get_user(session, username)
    mustSlowDown = False
    timeSinceLastAttempt = None
    if user is not None:
        lastAttempt = user.lastLoginAttempt
        if lastAttempt is not None:
            timeSinceLastAttempt = (datetime.now() - lastAttempt).total_seconds()
            mustSlowDown = timeSinceLastAttempt < options.min_login_retry
        verified = checkPassword(user, suppliedPassword) if not mustSlowDown else False
        user.lastLoginAttempt = datetime.now()
    else:
        verified = False

    if mustSlowDown:
        raise DoSError(timeSinceLastAttempt)

    return verified


def checkPassword(user, suppliedPassword):
    """Return True if and only if username is in the users DB
    and has correct password.

    When authenticating, use verify instead, which will perform
    other anti-DoS checks."""
    if user:
        LOG.debug("Calculating password hash (heavy)")
        return Hasher.verify(suppliedPassword, user.password)
    else:
        return False


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
