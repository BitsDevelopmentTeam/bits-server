# MUST be the first import
import bitsd.properties

import bitsd.pages as pages
import bitsd.websockets as websockets
import bitsd.remote as remote

from tornado.options import parse_command_line
import tornado.ioloop

def main():
    parse_command_line()

    pages.startserver()
    websockets.startserver()
    remote.startserver()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
