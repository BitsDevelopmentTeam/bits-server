#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from tornado.options import define

define("web_port",
    default=8008, help="Web server port", group='Networking'
)

define("ws_port",
    default=3389, help="WebSocket server port", group='Networking'
)

define("remote_port",
    default=8888, help="Port for fonera server.", group='Networking'
)

define("fonera_address",
    default="127.0.0.1", help="Fonera IP address.", group='Networking'
)

define("db_uri",
    default="sqlite:///test.db",
    help="DB URI, in the form `dialect:///username:password@host`",
    group='Config'
)

define("config",
    default='', help="Configuration file to read", group='Config'
)