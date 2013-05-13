#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Single-digit status request handlers.
"""

import tornado.web

from bitsd.persistence.logger import get_current_status

class StatusPageHandler(tornado.web.RequestHandler):
    """Get a single digit, indicating BITS status (open/closed)"""
    def get(self):
        status = get_current_status()
        self.write('1' if status.value == 'open' else '0')
        self.finish()
