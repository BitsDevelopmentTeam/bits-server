#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Query engine internals: functions to store, retrieve and count data
indipendently from the model.
"""

from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker
from tornado.options import options
from bitsd.common import LOG


#: Global session and engine used by all engine methods.
#: Call `connect()` to initialize.
Session = None
Engine = None

def connect():
    """
    Open a connection to DB using parameters  from bitsd.conf and command line.
    """
    global Session, Engine
    Engine = create_engine(options.db_uri, echo=options.log_queries)
    Session = sessionmaker(bind=Engine)


def persist(data):
    """Persist data to configured DB.

    **Note:** will log what's being persisted, so don't put clear text password
    into `__str__()`."""
    LOG.debug('Persisting data {}'.format(data))
    session = Session()
    session.add(data)
    session.commit()


def query_by_timestamp(model, limit=1, offset=0):
    """Query at most `limit` samples by timestamp.
    Default to `limit=1` (latest value)."""
    session = Session()
    query = session.query(model).order_by(desc(model.timestamp))
    if limit != 1:
        return query[offset:offset+limit]
    else:
        try:
            return query[offset]
        except IndexError:
            return None


def query_by_attribute(model, attribute, value, first=True):
    """Query all instances of `model` having `attribute == value`.
    If first is True, only first result will be returned (useful
    if attribute is a primary/candidate key)."""
    session = Session()
    query = session.query(model).filter_by(**{attribute: value})
    return query.first() if first else query


def count(model):
    """Returns count of `model` instances in DB."""
    session = Session()
    return session.query(model).count()

