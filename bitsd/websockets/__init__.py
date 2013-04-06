import tornado.web
from tornado.options import options

from .status import StatusHandler

from bitsd.common import LOG

def startserver():
    LOG.debug('Starting websocket server on port {}'.format(options.web_port))
    server = tornado.web.Application([
        (r'/', StatusHandler)
    ])
    server.listen(options.ws_port)
