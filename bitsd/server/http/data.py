#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web
from tornado.options import options

from bitsd.logger import get_current_status, get_current_temperature
from bitsd.logger import get_latest_temperature_samples


class DataPageHandler(tornado.web.RequestHandler):
    """Get BITS data in JSON, machine parseable."""
    def get(self):
        status = get_current_status()
        temp = get_current_temperature()
        latest_temp_samples = get_latest_temperature_samples()

        self.write({
            "status": status.jsondict(),
            "tempint": temp.jsondict(),
            "version": options.jsonver,
            #"msg": TODO,
            "tempinthist": [sample.jsondict() for sample in latest_temp_samples]
        })
