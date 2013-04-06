import tornado.web
from tornado.options import options

from .homepage import HomePageHandler
from .log import LogPageHandler

from bitsd.common import LOG

def startserver():
    LOG.debug('Starting web server on port {}'.format(options.web_port))
    server = tornado.web.Application([
            (r'/', HomePageHandler),
            (r'/storico', LogPageHandler),
        ],
    )
    server.listen(options.web_port)