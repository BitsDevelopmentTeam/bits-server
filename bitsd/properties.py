from tornado.options import define

# Define properties
define("web_port", default=8008, help="Web server port")
define("ws_port", default=3389, help="WebSocket server port")
