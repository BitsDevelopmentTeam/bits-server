from tornado.options import define, options
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.template

import logging

LOG = logging.getLogger('tornado.general')
LOG.setLevel('DEBUG')


define("web_port", default=8008, help="Web server port")
define("ws_port", default=3389, help="WebSocket server port")
define("template_dir", default="./templates", help="Directory to load templates from.")


class MessageNotifier(object):
    """Keeps a list of WebSocket handlers to notify with a message."""
    def __init__(self, name):
        self.clients = []
        self.name = name

    def register(self, client):
        """Add a new handler to the clients list."""
        LOG.debug('Adding client {} to {}'.format(client, self.name))
        self.clients.append(client)

    def unregister(self, client):
        """Remove the handler from the clients list."""
        LOG.debug('Removing client {} from {}'.format(client, self.name))
        self.clients.remove(client)

    def broadcast(self, message):
        """Notify all clients."""
        for client in self.clients:
            client.write_message(message)


class StatusHandler(tornado.websocket.WebSocketHandler):
    """Handler for POuL status via websocket"""

    QUEUE = MessageNotifier('Status handler queue')

    def open(self):
        """Register new handler with MessageNotifier."""
        StatusHandler.QUEUE.register(self)

    def on_message(self, message):
        """Disconnect clients sending data (they should not)."""
        LOG.info('Client {} sent a message so it has disconnected.'.format(self))

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.QUEUE.unregister(self)

    @staticmethod
    def broadcast(message):
        """Send a message to all connected clients."""
        StatusHandler.QUEUE.broadcast(message)


class PageHandler(tornado.web.RequestHandler):
    """Base class for all HTTP handlers, providing a global template engine."""
    LOADER = tornado.template.Loader(options.template_dir)


class HomePageHandler(PageHandler):
    def get(self):
        self.write(self.LOADER.load('homepage.html').generate())


class LogHandler(PageHandler):
    def get(self):
        self.write(self.LOADER.load('log.html').generate())


def main():
    tornado.options.parse_config_file('bitsd.conf')

    webserver = tornado.web.Application([
        (r'/', HomePageHandler),
        (r'/storico', LogHandler),
    ])

    statuserver = tornado.web.Application([
        (r'/', StatusHandler)
    ])

    LOG.debug('Starting web server on port {}'.format(options.web_port))
    webserver.listen(options.web_port)
    LOG.debug('Starting websocket status server on port {}'.format(options.web_port))
    statuserver.listen(options.ws_port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()