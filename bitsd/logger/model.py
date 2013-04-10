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

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, Float, DateTime, Enum

import datetime

Base = declarative_base()

class TemperatureSample(Base):
    __tablename__ = 'Temperature'

    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)
    value = Column(Float, primary_key=True)
    sensor = Column(Integer, nullable=False)
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, sensor, modified_by):
        self.value = value
        self.sensor = sensor
        self.modified_by = modified_by

    def __str__(self):
        return 'Temperature {.value}°C'.format(self)

    def jsondict(self):
        """Returns a JSON-parseable dictionary representing the object."""
        return {
            "timestamp": self.timestamp.isoformat(' '),
            "value": self.value,
            "modifiedby": self.modified_by,
            "sensor": self.sensor
        }


class Status(Base):
    __tablename__ = 'Status'

    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)
    value = Column(Enum('open', 'closed'), nullable=False)
    modified_by = Column(Enum('BITS', 'web'), nullable=False)

    def __init__(self, value, modified_by):
        self.value = value
        self.modified_by = modified_by

    def __str__(self):
        return 'Status {.value}'.format(self)

    def jsondict(self):
        """Returns a JSON-parseable dictionary representing the object."""
        return {
            "timestamp": self.timestamp.isoformat(' '),
            "modifiedby": self.modified_by,
            "value": self.value
        }
