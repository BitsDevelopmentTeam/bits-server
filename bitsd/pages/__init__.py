import tornado.web
from tornado.options import options

from .homepage import HomePageHandler
from .log import LogPageHandler

SERVER = tornado.web.Application([
        (r'/', HomePageHandler),
        (r'/storico', LogPageHandler),
    ],
    template_path=options.template_path,
)