#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

# NOTE: don't forget to register your handler in RemoteHandler.ACTIONS!

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
