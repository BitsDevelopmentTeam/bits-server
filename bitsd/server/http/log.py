#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.web

from bitsd.logger import get_latest_statuses

class LogPageHandler(tornado.web.RequestHandler):
    """Display and paginate log."""
    def get(self):
        self.render('log.html',
            latest_statuses=get_latest_statuses()
        )
