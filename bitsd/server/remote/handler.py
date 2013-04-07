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

from bitsd.common import LOG, unbase64


def handle_temperature_command(sensorid, value):
    sensorid = int(sensorid)
    value = float(value)
    LOG.info('Received temperature: sensorid={}, value={}'.format(sensorid, value))


def handle_status_command(status):
    status = int(status)
    LOG.info('Received status: {}'.format(status))


def handle_enter_command(id):
    id = int(id)
    LOG.info('Received enter command: id={}'.format(id))


def handle_leave_command(id):
    id = int(id)
    LOG.info('Received leave command: id={}'.format(id))


def handle_message_command(message):
    message = unbase64(message)
    LOG.info('Received message command: message={!r}'.format(message))


def handle_sound_command(id):
    id = int(id)
    LOG.info('Received sound command: id={}'.format(id))


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
        stream.read_until_close(self.handle_commands)

    def handle_commands(self, message):
        """Reacts to received commands (callback).
        Will split single commands, separate args and call appropriate handlers."""
        for command in message.split(b'\n'):
            if command:
                args = command.split(b' ')
                try:
                    handler = RemoteHandler.ACTIONS[args[0]]
                except KeyError:
                    LOG.warning('Remote received unknown command {}'.format(args))
                else:
                    # Execute handler (index 0) with args (index 1->end)
                    handler(*args[1:])
            else:
                LOG.warning('Remote received empty command.')
