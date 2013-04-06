import tornado.template
import tornado.web

from tornado.options import options

class PageHandler(tornado.web.RequestHandler):
    """Base class for all HTTP handlers, providing a global template engine."""
    LOADER = tornado.template.Loader('./templates')
