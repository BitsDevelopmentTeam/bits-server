#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Broadcast notifier via websocket push for BITSd events.
"""

from bitsd.common import LOG

class MessageNotifier(object):
    """Keeps a list of WebSocket handlers to notify with a message."""
    def __init__(self, name):
        self.clients = []
        self.name = name

    def register(self, client):
        """Add a new handler to the clients list."""
        LOG.debug('Adding client %r to %r', client, self.name)
        self.clients.append(client)

    def unregister(self, client):
        """Remove the handler from the clients list."""
        LOG.debug('Removing client %r from %r', client, self.name)
        self.clients.remove(client)

    def broadcast(self, message):
        """Notify all clients."""
        for client in self.clients:
            client.write_message(message)
