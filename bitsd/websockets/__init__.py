import tornado.web

from .status import StatusHandler

SERVER = tornado.web.Application([
    (r'/', StatusHandler)
])
