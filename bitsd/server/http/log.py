#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web

from bitsd.persistence.logger import get_latest_statuses

class LogPageHandler(tornado.web.RequestHandler):
    """Display and paginate log."""
    @tornado.web.removeslash
    def get(self, offset):
        # We can safely cast to int() because of the path regex \d+
        offset = int(offset) if offset is not None else 0

        self.render('log.html',
            latest_statuses=get_latest_statuses(offset=offset),
        )
