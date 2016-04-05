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

define("control_local_port",
    default=8888,
    help="Port for fonera server. Only if ws_usocket is not defined.",
    group='Networking'
)

define("control_local_usocket",
    default='', help="Unix socket the remote control will be listening on.",
    group="Networking"
)

define("control_local_address",
    default="127.0.0.1",
    help="The address the remote control will be bound to.",
    group='Networking'
)

define("control_remote_address",
    default="127.0.0.1",
    help="The address of the remote control unit (Fonera).",
    group="Networking"
)

define("reverse_proxied",
    default=False,
    help="Get remote IP address via X- headers (use when reverse proxied).",
    group="Networking"
)

define("db_uri",
    default="sqlite:///test.db",
    help="DB URI, in the form `dialect:///username:password@host`",
    group="Database"
)

define("connection_recycle_timeout",
    default=(60 * 60 * 7),  # 7 hours
    help="Prevents the pool from using a particular connection that is older than this parameter, in seconds",
    group="Database"
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
    default='bitsd/server/assets',
    help='Path to assets (for integrated server).',
    group='Internal'
)

define("min_login_retry",
    default=5,
    help="Min interval in seconds between two login attempts",
    group="Internal"
)

define("cookie_secret",
    default='Very random value, not like this',
    help='Secret used to generate securely hashed cookies',
    group='Internal'
)

define("cookie_max_age_days",
    default=1,
    help='Maximum age of the authentication cookie',
    group='Internal'
)


define("recaptcha_pubkey",
   default="pubkey",
   help="ReCaptcha public key",
   group="Internal"
)

define("recaptcha_privkey",
   default="privkey",
   help="ReCaptcha private key",
   group="Internal"
)

define("log_queries",
    default=False, help="Log DB queries.", group='Logging'
)

define("log_requests",
    default=True,
    help="Log HTTP requests. Non (200|304) responses are still logged.",
    group="Logging"
)

define("developer_mode",
    default=False,
    help="Auto reload modules on change. DO NOT enable in production.",
    group="Development"
)

define("usocket_uid",
    default=-1,
    help="UID to chown the unix sockets to.",
    group="Networking"
)

define("usocket_gid",
    default=-1,
    help="GID to chown the unix sockets to.",
    group="Networking"
)

define("usocket_mode",
    default=0o600,
    help="Permissions for chmod on the unix sockets",
    group="Networking"
)

define("mac_update_password",
   default="default",
   help="Authentication token for live presence updates",
   group="Networking"
)

define("mac_update_interval",
   default=0,
   help="Minimum number of seconds between two successive MAC updates.",
   group="Networking"
)

define("mac_hash_salt",
   default="Your key here",
   help="Salt string to combine for building the MAC addresses hashes.",
   group="Networking"
)
