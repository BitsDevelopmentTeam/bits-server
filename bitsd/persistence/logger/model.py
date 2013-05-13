# -*- coding: utf8 -*-
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Model for sensor persistence data.
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Float, DateTime, Enum

from datetime import datetime

from .. import Base


class TemperatureSample(Base):
    """Representation of a logged temperature sample."""
    __tablename__ = 'Temperature'

    timestamp = Column(DateTime, primary_key=True, default=datetime.utcnow)
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

    timestamp = Column(DateTime, primary_key=True, default=datetime.utcnow)
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
