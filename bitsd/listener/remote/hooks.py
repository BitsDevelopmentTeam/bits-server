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

# NOTE: don't forget to register your handler in RemoteListener.ACTIONS
#     : and in __all__ below!!

import base64

from bitsd.common import LOG
from bitsd.persistence.logger import log_temperature, log_status
from bitsd.persistence.logger import get_current_status
from bitsd.persistence.message import log_message
from bitsd.server.websockets.status import broadcast_status
from bitsd.client.fonera import Fonera
# Fixing Sphinx complaints
import bitsd.properties

from tornado.options import options

#: Proxy for BITS Fonera
FONERA = Fonera(options.fonera_host, options.remote_port)

__all__ = [
    'handle_temperature_command',
    'handle_status_command',
    'handle_enter_command',
    'handle_leave_command',
    'handle_message_command',
    'handle_sound_command'
]

def handle_temperature_command(sensorid, value):
    """Receives and log data received from remote sensor."""
    LOG.info('Received temperature: sensorid={}, value={}'.format(sensorid, value))
    try:
        sensorid = int(sensorid)
        value = float(value)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    temp = log_temperature(value, sensorid, 'BITS')
    broadcast_status(temp.jsondict(wrap=True)) # wrapped in a dict



def handle_status_command(status):
    """Update status.
    Will reject two identical and consecutive updates
    (prevents opening when already open and vice-versa)."""
    LOG.info('Received status: {}'.format(status))
    try:
        status = int(status)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command')
        return
    if status not in (0, 1):
        LOG.error('Non existent status {}, ignoring.'.format(status))
        return

    textstatus = 'open' if status == 1 else 'closed'
    curstatus = get_current_status()
    if curstatus is None or curstatus.value != textstatus:
        status = log_status(textstatus, 'BITS')
        broadcast_status(status.jsondict(wrap=True)) # wrapped in a dict
    else:
        LOG.error('BITS already open/closed! Ignoring.')


def handle_enter_command(userid):
    """Handles signal triggered when a new user enters."""
    LOG.info('Received enter command: id={}'.format(userid))
    try:
        userid = int(userid)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    LOG.error('handle_enter_command not implemented.')


def handle_leave_command(userid):
    """Handles signal triggered when a known user leaves."""
    LOG.info('Received leave command: id={}'.format(userid))
    try:
        userid = int(userid)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return

    LOG.error('handle_leave_command not implemented.')


def handle_message_command(message):
    """Handles message broadcast requests."""
    LOG.info('Received message command: message={!r}'.format(message))
    try:
        decodedmex = base64.b64decode(message)
    except TypeError:
        LOG.error('Received message is not valid base64: {!r}'.format(message))
    else:
        text = decodedmex.decode('utf8')
        #FIXME author ID
        message = log_message(0, text)
        broadcast_status(message.jsondict(wrap=True))
        FONERA.message(text)


def handle_sound_command(soundid):
    """Handles requests to play a sound."""
    LOG.info('Received sound command: id={}'.format(soundid))
    try:
        soundid = int(soundid)
    except ValueError:
        LOG.error('Wrong type for parameters in temperature command!')
        return
    else:
        FONERA.sound(soundid)
