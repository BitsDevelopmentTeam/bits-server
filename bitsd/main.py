# MUST be the first import
import bitsd.properties

import tornado.web
from tornado.options import options, parse_config_file

from bitsd.common import LOG

import bitsd.pages as pages
import bitsd.websockets as websockets
import bitsd.remote as remote

import sys

def main():
    # Load config if it is passed on the command line
    try:
        conf = sys.argv[1]
    except IndexError:
        print('No config file passed, loading defaults.', file=sys.stderr)
    else:
        parse_config_file(conf)

    pages.startserver()
    websockets.startserver()
    remote.startserver()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
