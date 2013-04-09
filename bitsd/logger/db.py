#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Actual DBMS proxy.
"""

from .model import TemperatureSample, Status, Base
from bitsd.common import LOG

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from tornado.options import options

# Call startdb() to initialize
ENGINE = None
Session = None


def start():
    """Will setup connection and ensure that all tables exist."""
    global ENGINE, Session

    LOG.info('Connecting to DB.')
    ENGINE = create_engine(options.db_uri, echo=options.log_queries)
    Session = sessionmaker(bind=ENGINE)

    # Create tables if they don't exist.
    LOG.info('Checking tables in the DB.')
    Base.metadata.create_all(ENGINE, checkfirst=True)


def persist(data):
    """Persist data to configured DB.
    WARNING will log what's being persisted, so don't put clear text password
    into `__str__()`."""
    LOG.debug('Persisting data {}'.format(data))
    session = Session()
    session.add(data)
    session.commit()


def query_by_timestamp(model, limit=1, offset=0):
    """Query at most `limit` samples by timestamp.
    Default to `limit=1` (latest value)."""
    session = Session()
    if limit != 1:
        return session.query(model).order_by(desc(model.timestamp))[offset:limit]
    else:
        return session.query(model).order_by(desc(model.timestamp))[offset]
