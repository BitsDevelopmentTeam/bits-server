#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

# MUST be the first import
import bitsd.properties

import bitsd.server.http as http
import bitsd.server.websockets as websockets
import bitsd.server.remote as remote
import bitsd.logger as logger

from tornado.options import parse_command_line
import tornado.ioloop

def main():
    parse_command_line()

    logger.startdb()
    http.startserver()
    websockets.startserver()
    remote.startserver()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
