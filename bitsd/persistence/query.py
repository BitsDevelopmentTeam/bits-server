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

from tornado.options import options

from .engine import persist, query_by_timestamp, count, query_by_attribute
from .models import TemperatureSample, Status, Message, Page

from datetime import datetime

## Exceptions ##

class SameTimestampException(Exception):
    pass

## Getters ##

def get_current_status():
    """Return a Status object representing most recent change."""
    return query_by_timestamp(Status, limit=1)


def get_current_temperature():
    """Return the most recent temperature sample."""
    return query_by_timestamp(TemperatureSample, limit=1)


def get_latest_temperature_samples():
    """Query 100 TemperatureSample by timestamp."""
    return query_by_timestamp(TemperatureSample, limit=100)


def get_latest_statuses(limit=20, offset=0):
    """Query last 20 Status by timestamp."""
    return query_by_timestamp(Status, limit=limit, offset=offset)


def get_number_of_statuses():
    """Get total number of logged statuses."""
    return count(Status)


def get_current_message():
    """Return message to display on website"""
    return query_by_timestamp(Message, limit=1)


def get_page(slug):
    """Get the page identified by the given slug."""
    return query_by_attribute(Page, 'slug', slug)


def get_latest_data():
    """Get recent data as a JSON-serializable dictionary."""
    status = get_current_status()
    temp = get_current_temperature()
    latest_temp_samples = get_latest_temperature_samples()
    latest_message = get_current_message()

    json_or_none = lambda data: data.jsondict() if data is not None else ""
    return {
        "status": json_or_none(status),
        "tempint": json_or_none(temp),
        "version": options.jsonver,
        "msg": json_or_none(latest_message),
        "tempinthist": [sample.jsondict() for sample in latest_temp_samples]
    }


## Loggers ##

def log_temperature(value, sensor, modified_by):
    """Add a temperature sample to the DB."""
    sample = TemperatureSample(value, sensor, modified_by)
    persist(sample)
    return sample


def log_status(status, modified_by):
    """Persist status to the DB."""
    sample = Status(status, modified_by)
    try:
        persist(sample)
    except: #FIXME
        raise SameTimestampException()
    return sample


def log_message(userid, message):
    """Persist message to DB."""
    message = Message(userid, message)
    persist(message)
    return message
