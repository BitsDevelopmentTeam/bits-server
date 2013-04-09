#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from tornado.options import options

from .handler import RemoteHandler

def start():
    fonera = RemoteHandler()
    # FIXME single threaded?
    #fonera.bind(options.fonera_port, options.fonera_address)
    #fonera.start(0)  # Forks multiple sub-processes
    fonera.listen(options.remote_port, options.fonera_address)
