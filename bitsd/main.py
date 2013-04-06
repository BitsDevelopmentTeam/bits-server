import tornado.options
import tornado.web

from bitsd.pages.homepage import HomePageHandler
from bitsd.pages.log import LogPageHandler
from bitsd.websockets.status import StatusHandler
from bitsd.common import LOG

import bitsd.properties

def main():
    tornado.options.parse_config_file('bitsd/bitsd.conf')

    webserver = tornado.web.Application([
            (r'/', HomePageHandler),
            (r'/storico', LogPageHandler),
        ],
        template_path='bitsd/templates',
    )

    statuserver = tornado.web.Application([
        (r'/', StatusHandler)
    ])

    LOG.debug('Starting web server on port {}'.format(
        tornado.options.options.web_port)
    )
    webserver.listen(tornado.options.options.web_port)

    LOG.debug('Starting websocket status server on port {}'.format(
        tornado.options.options.web_port)
    )
    statuserver.listen(tornado.options.options.ws_port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
