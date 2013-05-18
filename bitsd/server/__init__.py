#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Serve content to clients via TCP. All HTTP, WS etc. servers belong to here.
"""
from tornado.options import options

import bitsd.persistence.logger as logger
import bitsd.persistence.message as message

def get_latest_data():
    """Get recent data."""
    status = logger.get_current_status()
    temp = logger.get_current_temperature()
    latest_temp_samples = logger.get_latest_temperature_samples()
    latest_message = message.get_current_message()

    json_or_none = lambda data: data.jsondict() if data is not None else ""
    return {
        "status": json_or_none(status),
        "tempint": json_or_none(temp),
        "version": options.jsonver,
        "msg": json_or_none(latest_message),
        "tempinthist": [sample.jsondict() for sample in latest_temp_samples]
    }
