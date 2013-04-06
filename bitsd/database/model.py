#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Column, Integer, Float, DateTime

Base = declarative_base()

class TemperatureSample(Base):
    __tablename__ = 'Temperature'

    timestamp = Column(DateTime, primary_key=True)
    value = Column(Float, primary_key=True)
    sensor = Column(Integer)
    #modified_by = TODO

class Status(Base):
    __tablename__ = 'Status'

    timestamp = Column(DateTime, primary_key=True)
    #status = TODO
    #modified_by = TODO