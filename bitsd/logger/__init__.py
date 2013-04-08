#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from .db import persist
from .model import TemperatureSample, Status

from .db import startdb


def log_temperature(value, sensor, modified_by):
    """Add a temperature sample to the DB."""
    persist(TemperatureSample(value, sensor, modified_by))

def log_status(status, modified_by):
    """Persist status to the DB."""
    persist(Status(status, modified_by))
