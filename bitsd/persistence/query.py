#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Common query helpers. These are shortcut to queries performed often
by server engine.
"""
from sqlalchemy.exc import IntegrityError

from tornado.options import options

from .engine import persist, query_by_timestamp, count, query_by_attribute
from .models import TemperatureSample, Status, Message, Page, User


## Exceptions ##

class SameTimestampException(Exception):
    pass

## Getters ##

def get_current_status(session):
    """Return a Status object representing most recent change."""
    return query_by_timestamp(session, Status, limit=1)


def get_current_temperature(session):
    """Return the most recent temperature sample."""
    return query_by_timestamp(session, TemperatureSample, limit=1)


def get_latest_temperature_samples(session):
    """Query 100 TemperatureSample by timestamp."""
    return query_by_timestamp(session, TemperatureSample, limit=100)


def get_latest_statuses(session, limit=20, offset=0):
    """Query last 20 Status by timestamp."""
    return query_by_timestamp(session, Status, limit=limit, offset=offset)


def get_number_of_statuses(session):
    """Get total number of logged statuses."""
    return count(session, Status)


def get_current_message(session):
    """Return message to display on website"""
    return query_by_timestamp(session, Message, limit=1)


def get_page(session, slug):
    """Get the page identified by the given slug."""
    return query_by_attribute(session, Page, 'slug', slug)


def get_user(session, username):
    """Get user by name."""
    if not username:
        return None
    return query_by_attribute(session, User, 'name', username)


def get_user_from_id(session, userid):
    """Get user with specified userid"""
    return query_by_attribute(session, User, 'userid', userid)


def get_latest_data(session):
    """Get recent data as a JSON-serializable dictionary."""
    status = get_current_status(session)
    temp = get_current_temperature(session)
    latest_temp_samples = get_latest_temperature_samples(session)
    latest_message = get_current_message(session)

    json_or_none = lambda data: data.jsondict(wrap=False) if data is not None else ""
    return {
        "status": json_or_none(status),
        "tempint": json_or_none(temp),
        "version": options.jsonver,
        "msg": json_or_none(latest_message),
        "tempinthist": [sample.jsondict(wrap=False) for sample in latest_temp_samples]
    }


## Loggers ##

def log_temperature(session, value, sensor, modified_by):
    """Add a temperature sample to the DB."""
    return persist(session, TemperatureSample(value, sensor, modified_by))


def log_status(session, status, modified_by):
    """Persist status to the DB."""
    return persist(session, Status(status, modified_by))


def log_message(session, user, message):
    """Persist message by user to DB."""
    return persist(session, Message(user.userid, message))

