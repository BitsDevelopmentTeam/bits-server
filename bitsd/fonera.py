#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import tornado.iostream

import base64
import socket


class Fonera(tornado.iostream.IOStream):
    """Proxy object for controlling Fonera via BITS-miniprotocol."""

    def __init__(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        super().__init__(s)
        self.initialized = False
        self.host = host
        self.port = port
        self.connect((host, port), callback=self._handle_connection)

    def message(self, message):
        """
        A message is added to the list of messages shown on the display.

        >>> "message bG9sCg==\\n"
        """
        self.write("message {}\n".format(base64.b64encode(message)))

    def status(self, status):
        """
        Open or closes the BITS (respectively 1 or 0)

        >>> "status 1\\n"
        """
        try:
            status = int(status)
        except TypeError:
            status = 1 if status == 'open' else 0

        self.write("status {}\n".format(status))

    def sound(self, id):
        """
        Play a sound on the fonera.
        The parameter is an index into a list of predefined sounds.
        Sad trombone anyone?

        >>> "sound 0\\n"
        """
        self.write("sound {}\n".format(status))

    def _handle_connection(self):
        """Connection callback: log and set initialized flag."""
        LOG.info('Connected to Fonera on {.host}:{.port}'.format(self))
        self.initialized = True
