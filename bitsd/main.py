# MUST be the first import
import bitsd.properties

import tornado.web
from tornado.options import options, parse_config_file

from bitsd.common import LOG

import bitsd.pages as pages
import bitsd.websockets as websockets

import sys

def main():
    # Load config if it is passed on the command line
    try:
        conf = sys.argv[1]
    except IndexError:
        print('No config file passed, loading defaults.', file=sys.stderr)
    else:
        parse_config_file(conf)

    LOG.debug('Starting web server on port {}'.format(options.web_port))
    pages.SERVER.listen(options.web_port)

    LOG.debug('Starting websocket server on port {}'.format(options.web_port))
    websockets.SERVER.listen(options.ws_port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
