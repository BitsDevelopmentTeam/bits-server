# MUST be the first import
import bitsd.properties

import tornado.web
from tornado.options import options, parse_config_file

from bitsd.common import LOG

import bitsd.pages as pages
import bitsd.websockets as websockets

import sys

def main():
    parse_config_file(sys.argv[1])

    LOG.debug('Starting web server on port {}'.format(options.web_port))
    pages.SERVER.listen(options.web_port)

    LOG.debug('Starting websocket server on port {}'.format(options.web_port))
    websockets.SERVER.listen(options.ws_port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
