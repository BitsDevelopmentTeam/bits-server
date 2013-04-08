#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

#import tornado.tcpserver TODO Tornado 3.0
import tornado.netutil
from tornado.options import options

from bitsd.common import LOG
from bitsd.server.remote.hooks import *


class RemoteHandler(tornado.netutil.TCPServer):
    """Handle incoming commands via BITS mini protocol."""

    ACTIONS = {
        b'temperature': handle_temperature_command,
        b'status': handle_status_command,
        b'enter': handle_enter_command,
        b'leave': handle_leave_command,
        b'message': handle_message_command,
        b'sound': handle_sound_command,
    }

    def handle_stream(self, stream, address):
        """Handles inbound TCP connections asynchronously."""
        if address[0] != options.fonera_address:
            LOG.error("Remote received commands from `{}`, expected from `{}`. Ignoring.".format(
            address, options.fonera_address))
            return
        self.stream = stream
        self.stream.read_until(b'\n', self.handle_command)

    def handle_command(self, command):
        """Reacts to received commands (callback).
        Will separate args and call appropriate handlers."""

        # Meanwhile, go on with commands...
        self.stream.read_until(b'\n', self.handle_command)

        if command:
            args = command.split(b' ')
            try:
                handler = RemoteHandler.ACTIONS[args[0]]
            except KeyError:
                LOG.warning('Remote received unknown command {}'.format(args))
            else:
                # Execute handler (index 0) with args (index 1->end)
                try:
                    handler(*args[1:])
                except TypeError:
                    LOG.error('Command {} called with wrong number of args')
        else:
            LOG.warning('Remote received empty command.')
