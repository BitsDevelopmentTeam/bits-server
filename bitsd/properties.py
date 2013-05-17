#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Define properties as shown in the `--help` page and in the config file.
"""

from tornado.options import define


define("web_port",
    default=8008, help="Web server port. Only if web_usocket is not defined.",
    group='Networking'
)

define("web_usocket",
    default='', help="Unix socket the web server will be listening on.",
    group="Networking"
)

define("ws_port",
    default=3389,
    help="WebSocket server port. Only if ws_usocket is not defined.",
    group='Networking'
)

define("ws_usocket",
    default='', help="Unix socket the WebSocket server will be listening on.",
    group="Networking"
)

define("remote_port",
    default=8888,
    help="Port for fonera server. Only if ws_usocket is not defined.",
    group='Networking'
)

define("remote_usocket",
    default='', help="Unix socket the remote control will be listening on.",
    group="Networking"
)

define("remote_address",
    default="127.0.0.1",
    help="The address the remote control will be bound to.",
    group='Networking'
)

define("fonera_host",
    default="127.0.0.1",
    help="The address of the remote control unit (Fonera).",
    group="Networking"
)

define("db_uri",
    default="sqlite:///test.db",
    help="DB URI, in the form `dialect:///username:password@host`",
    group='Config'
)

define("config",
    default='', help="Configuration file to read", group='Config'
)

define("jsonver",
    default=3, help="JSON data protocol version", group='Internal'
)

define("mdescape",
    default=True,
    help="Escape literal HTML in Markdown source.", group='Internal'
)

define("assets_path",
    default='bitsd/server/http/assets',
    help='Path to assets (for integrated server).',
    group='Internal'
)

define("log_queries",
    default=False, help="Log DB queries.", group='Debug')

define("developer_mode",
    default=False,
    help="Auto reload modules on change. DO NOT enable in production.",
    group="Development"
)

define("usocket_uid",
    default=1000,
    help="UID to chown the unix sockets to.",
    group="Networking"
)

define("usocket_gid",
    default=1000,
    help="GID to chown the unix sockets to.",
    group="Networking"
)

define("usocket_mode",
    default=0o600,
    help="Permissions for chmod on the unix sockets",
    group="Networking"
)
