#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Send BITS-miniprotocol notification messages to remote host.
"""

import base64
from bitsd.persistence.models import Status

import handlers


def send_message(text):
    """
    A message is added to the list of messages shown on the Fonera display.
    """
    handlers.send("message {}\n".format(base64.b64encode(text)))


def send_status(value):
    """
    Send open or close status to the BITS Fonera.
    Status can be either 0 / 1 or Status.CLOSED / Status.OPEN
    """
    try:
        value = int(value)
    except ValueError:
        value = 1 if value == Status.OPEN else 0

    handlers.send("status {}\n".format(value))


def send_sound(soundid):
    """
    Play a sound on the fonera.
    The parameter is an index into a list of predefined sounds.
    Sad trombone anyone?
    """
    handlers.send("sound {}\n".format(soundid))
