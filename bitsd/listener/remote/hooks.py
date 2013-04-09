#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Hooks called by bitsd.listener.remote.RemoteListener to handle commands.
"""

# NOTE: don't forget to register your handler in RemoteListener.ACTIONS!

from bitsd.common import LOG, unbase64
from bitsd.logger import log_temperature, log_status
from bitsd.server.websockets.status import broadcast_status
from bitsd.fonera import Fonera

from tornado.options import options


FONERA = Fonera(options.fonera_host, options.remote_port)


def handle_temperature_command(sensorid, value):
    sensorid = int(sensorid)
    value = float(value)
    LOG.info('Received temperature: sensorid={}, value={}'.format(sensorid, value))
    log_temperature(sensorid, value, 'BITS')


def handle_status_command(status):
    # TODO catch value error
    status = int(status)
    textstatus = 'open' if status == 1 else 'closed'
    LOG.info('Received status: {}'.format(status))
    log_status(textstatus, 'BITS')
    broadcast_status(textstatus)


def handle_enter_command(id):
    id = int(id)
    LOG.info('Received enter command: id={}'.format(id))
    LOG.error('handle_enter_command not implemented.')


def handle_leave_command(id):
    id = int(id)
    LOG.info('Received leave command: id={}'.format(id))
    LOG.error('handle_leave_command not implemented.')


def handle_message_command(message):
    message = unbase64(message)
    LOG.info('Received message command: message={!r}'.format(message))
    FONERA.message(message)


def handle_sound_command(id):
    id = int(id)
    LOG.info('Received sound command: id={}'.format(id))
    FONERA.sound(id)