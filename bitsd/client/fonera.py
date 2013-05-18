#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Classes and helpers needed to send commands to the Fonera remote.
"""

import tornado.iostream

import base64
import socket

from bitsd.common import LOG

# TODO handle disconnect/reconnect with StreamClosedError
class Fonera(tornado.iostream.IOStream):
    """Proxy object for controlling Fonera via BITS-miniprotocol."""

    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        super(Fonera, self).__init__(sock)
        self.initialized = False
        self.host = host
        self.port = port
        self.connect((host, port), callback=self._handle_connection)

    def message(self, message):
        """
        A message is added to the list of messages shown on the display.

        >>> "message bG9sCg==\\n"
        """
        try:
            self.write("message {}\n".format(base64.b64encode(message)))
        except tornado.iostream.StreamClosedError as error:
            LOG.error('Could not push message to Fonera! {}'.format(error))
            #TODO Handle reconnection

    def status(self, status):
        """
        Open or closes the BITS (respectively 1 or 0)

        >>> "status 1\\n"
        """
        try:
            status = int(status)
        except TypeError:
            status = 1 if status == 'open' else 0

        try:
            self.write("status {}\n".format(status))
        except tornado.iostream.StreamClosedError as error:
            LOG.error('Could not push status to Fonera! {}'.format(error))
            #TODO Handle reconnection

    def sound(self, soundid):
        """
        Play a sound on the fonera.
        The parameter is an index into a list of predefined sounds.
        Sad trombone anyone?

        >>> "sound 0\\n"
        """
        try:
            self.write("sound {}\n".format(soundid))
        except tornado.iostream.StreamClosedError as error:
            LOG.error('Could not push sound to Fonera! {}'.format(error))
            #TODO Handle reconnection

    def _handle_connection(self):
        """Connection callback: log and set initialized flag."""
        LOG.info('Connected to Fonera on {.host}:{.port}'.format(self))
        self.initialized = True
