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
    default=8008, help="Web server port", group='Networking'
)

define("ws_port",
    default=3389, help="WebSocket server port", group='Networking'
)

define("remote_port",
    default=8888, help="Port for fonera server.", group='Networking'
)

define("fonera_host",
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
