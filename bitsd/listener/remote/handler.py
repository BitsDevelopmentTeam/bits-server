#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#


"""
TCP server receiving raw messages and invoke correct handlers
(from module `.hooks`)
"""

import tornado.tcpserver
from tornado.options import options

from bitsd.common import LOG

from .hooks import *


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

    def __init__(self):
        super(RemoteListener, self).__init__()
        self.stream = None

    def handle_stream(self, stream, address):
        """Handles inbound TCP connections asynchronously."""
        if address[0] != options.fonera_host:
            LOG.error(("Remote received commands from `{}`, "
                "expected from `{}`. Ignoring.").format(
            address, options.fonera_host))
            return
        self.stream = stream
        self.stream.read_until(b'\n', self.handle_command)

    def handle_command(self, command):
        """Reacts to received commands (callback).
        Will separate args and call appropriate handlers."""

        # Meanwhile, go on with commands...
        self.stream.read_until(b'\n', self.handle_command)

        command = command.strip('\n')

        if command:
            args = command.split(b' ')
            try:
                handler = RemoteListener.ACTIONS[args[0]]
            except KeyError:
                LOG.warning('Remote received unknown command {}'.format(args))
            else:
                # Execute handler (index 0) with args (index 1->end)
                try:
                    handler(*args[1:])
                except TypeError:
                    LOG.error(
                        'Command {} called with wrong number of args'.format(
                            args[0]))
        else:
            LOG.warning('Remote received empty command.')
