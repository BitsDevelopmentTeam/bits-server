#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

import logging
import base64

# Get logger
LOG = logging.getLogger('tornado.general')

def unbase64(message):
    try:
        decodedmex = base64.b64decode(message)
    except TypeError:
        LOG.error('Received message is not valid base64: {!r}'.format(message))
    else:
        return decodedmex.decode('utf8')
