# -*- coding: utf8 -*-
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Models for persisted data.
"""

import re
from datetime import datetime

from sqlalchemy import Column, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, Float, DateTime, Enum, Text, BigInteger, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

from . import engine

#: Base class for declared models.
from tornado.escape import xhtml_escape

Base = declarative_base()


def check():
    """Check if all the tables are present in the DB, create them otherwise."""
    Base.metadata.create_all(engine.Engine, checkfirst=True)


class TemperatureSample(Base):
    """Representation of a logged temperature sample."""
    __tablename__ = 'Temperature'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    value = Column(Float, nullable=False)
    sensor = Column(Integer, primary_key=True)
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, sensor, modified_by):
        self.value = value
        self.sensor = sensor
        self.modified_by = modified_by

    def __str__(self):
        return 'Temperature {.value}°C'.format(self)

    def jsondict(self, wrap=True):
        """Return a JSON-serializable dictionary representing the object"""
        data = {
            "timestamp": self.timestamp.isoformat(' '),
            "value": self.value,
            "modifiedby": self.modified_by,
            "sensor": self.sensor
        }
        if wrap:
            return {"tempint": data}
        else:
            return data


class Status(Base):
    """Representation of a logged status change."""
    __tablename__ = 'Status'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    OPEN = 'open'
    CLOSED = 'closed'
    AWAY = 'away'

    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    value = Column(
        Enum(OPEN, CLOSED, AWAY),
        nullable=False
    )
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, modified_by):
        self.value = value
        self.modified_by = modified_by

    def __str__(self):
        return 'Status {.value}'.format(self)

    def jsondict(self, wrap=True):
        """Return a JSON-serializable dictionary representing the object"""
        data = {
            "timestamp": self.timestamp.isoformat(' '),
            "modifiedby": self.modified_by,
            "value": self.value
        }
        if wrap:
            return {'status': data}
        else:
            return data


class Message(Base):
    """Representation of a broadcast message.
    Access the author object with `.author`"""
    __tablename__ = 'Message'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    userid = Column(Integer, ForeignKey("User.userid"), primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    message = Column(Text, nullable=False)

    author = relationship("User")

    def __init__(self, userid, message):
        self.userid = userid
        self.message = message

    def jsondict(self, wrap=True, escape=True):
        """Return a JSON-serializable dictionary representing the object.

        When escape is True, the HTML entities in the message body are escaped."""
        data = {
            'user': self.author.name,
            'timestamp': self.timestamp.isoformat(' '),
            'value': xhtml_escape(self.message) if escape else self.message,
        }
        return {'message': data} if wrap else data


class Page(Base):
    """Representation of a wiki page."""
    __tablename__ = 'Pages'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    slug = Column(String(length=100), primary_key=True)
    title = Column(String(length=100), nullable=False)
    body = Column(UnicodeText, nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.slug = Page.slugify(title)

    def __str__(self):
        return 'Page: {.title}'.format(self)

    def jsondict(self, wrap=True):
        """Return a JSON-serializable dictionary representing the object"""
        data = {
            "title": self.title,
            "body": self.body,
            "slug": self.slug
        }
        return {"page": data} if wrap else data

    @staticmethod
    def slugify(title):
        """Turn a title into a HTTP-friendly slug: lowercase, all
        non-letters are replaced by a dash."""
        # TODO test regex
        # Strip will remove trailing '-'
        return re.sub(r'[^\w]+', '-', title).strip('-').lower()


class User(Base):
    """User name/password hash entity."""
    __tablename__ = 'User'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    userid = Column(Integer, primary_key=True)
    name = Column(String(length=256), unique=True, nullable=False)
    password = Column(String(length=512), nullable=False)

    def __init__(self, name, pwhash):
        self.name = name
        self.password = pwhash

    def __str__(self):
        return '{self.name}: {self.password}'.format(self=self)


class LoginAttempt(Base):
    """Holds IP address, user and timestamp for failed login attempts.

     Failed attempts are kept in order to prevent DoS and bruteforcing attacks."""
    __tablename__ = 'LoginAttempt'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}

    id = Column(Integer, primary_key=True)
    username = Column(String(length=256), nullable=True)
    ipaddress = Column(String(length=64), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)

    UniqueConstraint('username', 'ipaddress', name='user_ip_key')
    Index('user_IP_login_attempt_idx', username, ipaddress, unique=True)

    def __init__(self, username, ipaddress):
        self.username = username
        self.ipaddress = ipaddress

    def __str__(self):
        return 'Failed attempt for `{self.username}` from {self.ipaddress} at {self.timestamp}'.format(self=self)
