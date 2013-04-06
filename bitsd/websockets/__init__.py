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