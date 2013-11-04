#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#


"""
TCP server receiving raw messages and invoke correct handlers
(from module `.hooks`). Listens for remote commands on BITS-miniprotocol
and dispatches to Fonera via bitsd.client.fonera.Fonera proxy.
"""

import tornado.tcpserver
from tornado.options import options
from tornado.iostream import StreamClosedError

from bitsd.common import LOG
from bitsd.persistence.models import Status
from .hooks import *

import base64


class RemoteListener(tornado.tcpserver.TCPServer):
    """
    Handle incoming commands via BITS mini protocol.

    Trying to do something KISS.
    Commands are rpc-like: function name and eventual args, separated by spaces.
    One command per line, "\\n" as line separator.
    Numeric argument are printed as-is, string arguments are encoded in base64.

    **status** <int>
        Parameter 0 is "closed", 1 is "open".

        >>> "status 1\\n"

    **enter** <int>
        One person is added to the list of persone in sede.
        The first parameter is the number inserted on the numeric keypad.

        >>> "enter 5\\n"

    **leave** <int>
        One person is removed from the list of persone in sede.
        The first parameter is the number inserted on the numeric keypad.

        >>> "leave 5\\n"

    **message** <string>
        A message is added to the list of messages shown on the display.

        >>> "message bG9sCg==\\n"

    **sound** <int>
        Play a sound on the fonera.
        The parameter is an index into a list of predefined
        sounds. Sad trombone anyone?

        >>> "sound 0\\n"
    """

    ACTIONS = {
        b'temperature': handle_temperature_command,
        b'status': handle_status_command,
        b'enter': handle_enter_command,
        b'leave': handle_leave_command,
        b'message': handle_message_command,
        b'sound': handle_sound_command,
    }

    STREAM = None

    def __init__(self):
        super(RemoteListener, self).__init__()
        self.STREAM = None

    def handle_stream(self, stream, address):
        """Handles inbound TCP connections asynchronously."""
        if address[0] != options.control_remote_address:
            LOG.error((
                "Remote received commands from `{}`, "
                "expected from `{}`. Ignoring.").format(
                    address,
                    options.control_remote_address
            ))
            return
        if self.STREAM is not None:
            LOG.warning("New connection from Fonera, closing the previous one.")
            self.STREAM.close()
        self.STREAM = stream
        self.STREAM.read_until(b'\n', self.handle_command)

    @staticmethod
    def message(message):
        """
        A message is added to the list of messages shown on the Fonera display.
        """
        RemoteListener.send("message {}\n".format(base64.b64encode(message)))

    @staticmethod
    def status(status):
        """
        Send open or close status to the BITS Fonera.
        Status can be either 0 / 1 or Status.CLOSED / Status.OPEN
        """
        try:
            status = int(status)
        except ValueError:
            status = 1 if status == Status.OPEN else 0

        RemoteListener.send("status {}\n".format(status))

    @staticmethod
    def sound(soundid):
        """
        Play a sound on the fonera.
        The parameter is an index into a list of predefined sounds.
        Sad trombone anyone?
        """
        RemoteListener.send("sound {}\n".format(soundid))

    @staticmethod
    def send(string):
        try:
            RemoteListener.STREAM.write(string)
        except StreamClosedError as error:
            LOG.error('Could not push message to Fonera! {}'.format(error))

    def handle_command(self, command):
        """Reacts to received commands (callback).
        Will separate args and call appropriate handlers."""

        # Meanwhile, go on with commands...
        self.STREAM.read_until(b'\n', self.handle_command)

        command = command.strip('\n')

        if command:
            args = command.split(b' ')
            action = args[0]
            try:
                handler = RemoteListener.ACTIONS[action]
            except KeyError:
                LOG.warning('Remote received unknown command {}'.format(args))
            else:
                # Execute handler (index 0) with args (index 1->end)
                try:
                    args[0] = self
                    handler(*args)
                except TypeError:
                    LOG.error(
                        'Command {} called with wrong number of args'.format(action)
                    )
        else:
            LOG.warning('Remote received empty command.')
