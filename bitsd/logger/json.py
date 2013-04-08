#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import json
import datetime

from sqlalchemy.types import Enum
from tornado.options import options

from .model import TemperatureSample, Status
from . import get_current_status, get_current_temperature
from . import get_latest_temperature_samples


class JSONEncoder(json.JSONEncoder):
    """JSON encoder expanded to support all the types defined in `.models`"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return repr(obj)
        elif isinstance(obj, Status):
            return {
                "timestamp": obj.timestamp,
                "modifiedby": obj.modified_by,
                "value": obj.value,
            }
        elif isinstance(obj, TemperatureSample):
            return {
                "timestamp": obj.timestamp,
                "value": obj.value,
            }


def dump_latest():
    """Dump latest data in a form useful for export."""
    return JSONEncoder().encode({
        "status": get_current_status(),
        "tempint": get_current_temperature(),
        "version": options.jsonver,
        #"msg": TODO,
        "tempinthist": get_latest_temperature_samples(),
    })
