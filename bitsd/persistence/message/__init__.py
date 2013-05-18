#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Persists broadcast messages and offers some helper functions for managing
message retrieval.
"""

from .. import persist, query_by_timestamp
from .model import Message


def get_current_message():
    """Return message to display on website"""
    return query_by_timestamp(Message, limit=1)


def log_message(userid, message):
    """Persist message to DB."""
    message = Message(userid, message)
    persist(message)
    return message

