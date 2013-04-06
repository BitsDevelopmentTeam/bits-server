import tornado.websocket

from bitsd.websockets.common import MessageNotifier

class StatusHandler(tornado.websocket.WebSocketHandler):
    """Handler for POuL status via websocket"""

    QUEUE = MessageNotifier('Status handler queue')

    def open(self):
        """Register new handler with MessageNotifier."""
        StatusHandler.QUEUE.register(self)

    def on_message(self, message):
        """Disconnect clients sending data (they should not)."""
        LOG.info('Client {} sent a message so it has been disconnected.'.format(self))

    def on_close(self):
        """Unregister this handler when the connection is closed."""
        StatusHandler.QUEUE.unregister(self)

    @staticmethod
    def broadcast(message):
        """Send a message to all connected clients."""
        StatusHandler.QUEUE.broadcast(message)
