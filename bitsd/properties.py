from tornado.options import define

define("web_port", default=8008, help="Web server port")
define("ws_port", default=3389, help="WebSocket server port")

define("fonera_port", default=8888, help="Port for fonera server.")
define("fonera_address", default="127.0.0.1", help="Fonera IP address.")