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

from contextlib import contextmanager
from sqlalchemy import desc, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session
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
    Engine = create_engine(
        options.db_uri,
        pool_recycle=options.connection_recycle_timeout,
        echo=options.log_queries
    )
    session_factory = sessionmaker(bind=Engine)
    Session = scoped_session(session_factory)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        LOG.error("Integrity error in DB, rolling back: {}".format(e))
        session.rollback()
    except:
        LOG.error("Error in DB, rolling back.")
        session.rollback()
        raise
    finally:
        session.close()


def persist(session, data):
    """Persist data to configured DB and return persisted object
    in a consistent state.

    **Note:** will log what's being persisted, so don't put clear text password
    into `__str__()`."""
    LOG.debug('Persisting data {}'.format(data))
    session.add(data)
    return data


def delete(session, data):
    """Delete data from DB."""
    LOG.debug('Deleting {}'.format(data))
    session.delete(data)


def query_by_timestamp(session, model, limit=1, offset=0):
    """Query at most `limit` samples by timestamp.
    Default to `limit=1` (latest value)."""
    query = session.query(model).order_by(desc(model.timestamp))
    if limit != 1:
        result = query[offset:offset+limit]
    else:
        try:
            result = query[offset]
        except IndexError:
            result = None
    return result


def query_by_attribute(session, model, attribute, value, first=True):
    """Query all instances of `model` having `attribute == value`.
    If first is True, only first result will be returned (useful
    if attribute is a primary/candidate key)."""
    query = session.query(model).filter_by(**{attribute: value})
    result = query.first() if first else query
    return result


def count(session, model):
    """Returns count of `model` instances in DB."""
    result = session.query(model).count()
    return result

