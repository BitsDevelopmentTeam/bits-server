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
import bitsd.listener.remote as remote
import bitsd.logger as logger

from bitsd.common import LOG

from tornado.options import parse_command_line, options
import tornado.ioloop

import signal
import time

# Signal code adapted from https://gist.github.com/kachayev/1387470

def sig_handler(sig, frame):
    """Catch signal and init callback.

    Reference:
    http://codemehanika.org/blog/2011-10-28-graceful-stop-tornado.html
    """
    LOG.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    """Stop server and add callback to stop i/o loop."""
    io_loop = tornado.ioloop.IOLoop.instance()
    LOG.info('Shutting down in 2 seconds')
    io_loop.add_timeout(time.time() + 2, io_loop.stop)


def main():
    """Entry point for bitsd."""
    parse_command_line()

    LOG.info('Starting Logger')
    logger.start()
    LOG.info('Starting HTTP server on port {}'.format(options.web_port))
    http.start()
    LOG.info('Starting Websocket server on port {}'.format(options.ws_port))
    websockets.start()
    LOG.info('Starting remote control on port {}'.format(options.remote_port))
    LOG.info('Remote control IP is {}'.format(options.fonera_address))
    remote.start()

    # Add signal handlers...
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.instance().start()
