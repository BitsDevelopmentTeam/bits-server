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

from bitsd.common import LOG
from bitsd.persistence.logger import log_temperature, log_status, get_latest_data
from bitsd.server.websockets.status import broadcast_status
from bitsd.client.fonera import Fonera

# Fixing Sphinx complaints
import bitsd.properties
from tornado.options import options


FONERA = Fonera(options.fonera_host, options.remote_port)


def handle_temperature_command(sensorid, value):
    LOG.info('Received temperature: sensorid={}, value={}'.format(sensorid, value))
    try:
        sensorid = int(sensorid)
        value = float(value)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    temp = log_temperature(value, sensorid, 'BITS')
    # Return wrapped in dict
    broadcast_status(temp.jsondict(wrap=True))



def handle_status_command(status):
    LOG.info('Received status: {}'.format(status))
    try:
        status = int(status)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command')
        return
    if status not in (0,1):
        LOG.error('Non existent status {}, ignoring.'.format(status))
        return

    textstatus = 'open' if status == 1 else 'closed'
    status = log_status(textstatus, 'BITS')
    # Return wrapped in dict
    broadcast_status(status.jsondict(wrap=True))


def handle_enter_command(id):
    LOG.info('Received enter command: id={}'.format(id))
    try:
        id = int(id)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    LOG.error('handle_enter_command not implemented.')


def handle_leave_command(id):
    LOG.info('Received leave command: id={}'.format(id))
    try:
        id = int(id)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    LOG.error('handle_leave_command not implemented.')


def handle_message_command(message):
    LOG.info('Received message command: message={!r}'.format(message))
    try:
        decodedmex = base64.b64decode(message)
    except TypeError:
        LOG.error('Received message is not valid base64: {!r}'.format(message))
    else:
        message = decodedmex.decode('utf8')

    FONERA.message(message)


def handle_sound_command(id):
    LOG.info('Received sound command: id={}'.format(id))
    try:
        id = int(id)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    FONERA.sound(id)