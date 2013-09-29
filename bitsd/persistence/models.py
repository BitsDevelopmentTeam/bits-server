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

from sqlalchemy import Column
from sqlalchemy.types import Integer, Float, DateTime, Enum, Text, BigInteger, String, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

from . import engine

#: Base class for declared models.
Base = declarative_base()


def check():
    """Check if all the tables are present in the DB, create them otherwise."""
    Base.metadata.create_all(engine.Engine, checkfirst=True)


class TemperatureSample(Base):
    """Representation of a logged temperature sample."""
    __tablename__ = 'Temperature'

    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    value = Column(Float, primary_key=True)
    sensor = Column(Integer, nullable=False)
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, sensor, modified_by):
        self.value = value
        self.sensor = sensor
        self.modified_by = modified_by

    def __str__(self):
        return 'Temperature {.value}°C'.format(self)

    def jsondict(self, wrap=False):
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

    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    value = Column(Enum('open', 'closed'), nullable=False)
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, modified_by):
        self.value = value
        self.modified_by = modified_by

    def __str__(self):
        return 'Status {.value}'.format(self)

    def jsondict(self, wrap=False):
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

    def get_timestamp(self):
        """Return the timestamp value of the object"""
        return self.timestamp.isoformat(' ')


class Message(Base):
    """Representation of a broadcast message."""
    __tablename__ = 'Message'

    userid = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.now)
    message = Column(Text, nullable=False)

    def __init__(self, userid, message):
        self.userid = userid
        self.message = message

    def jsondict(self, wrap=False):
        """Return a JSON-serializable dictionary representing the object"""
        data = {
            'user': self.userid,
            'timestamp': self.timestamp.isoformat(' '),
            'value': self.message,
        }
        return {'message': data} if wrap else data


class Page(Base):
    """Representation of a wiki page."""
    __tablename__ = 'Pages'

    slug = Column(String(length=100), primary_key=True)
    title = Column(String(length=100), nullable=False)
    body = Column(UnicodeText, nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.slug = Page.slugify(title)

    def __str__(self):
        return 'Page: {.title}'.format(self)

    def jsondict(self):
        """Return a JSON-serializable dictionary representing the object"""
        return {
            "title": self.title,
            "body": self.body,
            "slug": self.slug
        }

    @staticmethod
    def slugify(title):
        """Turn a title into a HTTP-friendly slug: lowercase, all
        non-letters are replaced by a dash."""
        # TODO test regex
        # Strip will remove trailing '-'
        return re.sub(r'[^\w]+', '-', title).strip('-').lower()
