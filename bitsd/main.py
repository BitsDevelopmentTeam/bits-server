#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
BITSd entry point and unix signal handlers.
"""

# MUST be the first import, DO NOT REMOVE
import bitsd.properties

import bitsd.server as server
import bitsd.listener as listener
import bitsd.persistence as persistence

from bitsd.common import LOG

from tornado.options import parse_command_line
from tornado.options import parse_config_file, options
from tornado.log import enable_pretty_logging

import tornado.ioloop

import signal
import time
import sys
import logging

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
    enable_pretty_logging()

    try:
        parse_config_file('/etc/bitsd.conf')
    except IOError:
        LOG.warning('Config file not found, using defaults and command line.')

    try:
        parse_command_line()
    except tornado.options.Error as error:
        sys.stderr.write('{}\n'.format(error))
        sys.exit(0)

    persistence.start()
    server.start()
    listener.start()

    # Add signal handlers...
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    if not options.log_requests:
        logging.getLogger("tornado.access").setLevel(logging.WARNING)

    tornado.ioloop.IOLoop.instance().start()
