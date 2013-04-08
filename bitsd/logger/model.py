#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, Float, DateTime, Enum

import datetime

Base = declarative_base()

class TemperatureSample(Base):
    __tablename__ = 'Temperature'

    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)
    value = Column(Float, primary_key=True)
    sensor = Column(Integer)
    modified_by = Enum('BITS', 'web')

    def __init__(self, value, sensor, modified_by):
        self.value = value
        self.sensor = sensor
        self.modified_by = modified_by


class Status(Base):
    __tablename__ = 'Status'

    timestamp = Column(DateTime, primary_key=True, default=datetime.datetime.utcnow)
    status = Enum('open', 'closed')
    modified_by = Enum('BITS', 'web')

    def __init__(self, status, modified_by):
        self.status = status
        self.modified_by = modified_by
