#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Models for stored broadcast messages.
"""

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.types import Text, BigInteger, DateTime

from .. import Base

class Message(Base):
    """Representation of a broadcast message."""
    __tablename__ = 'Message'

    userid = Column(BigInteger, primary_key=True)
    timestamp = Column(DateTime, primary_key=True, default=datetime.utcnow)
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
