from ..common import LOG

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
