#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from passlib.hash import sha512_crypt as Hasher
from bitsd.persistence.query import get_user
from bitsd.persistence.models import User
from bitsd.persistence.engine import persist, delete


def verify(session, username, password):
    """Return True if and only if username is in the users DB
    and has correct password."""
    entity = get_user(session, username)
    if entity:
        return Hasher.verify(password, entity.hash)
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
