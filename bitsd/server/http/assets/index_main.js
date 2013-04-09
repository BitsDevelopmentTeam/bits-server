main(function (require) {
    "use strict";

    var Handler = require("handler").Handler,
        browserHandler = require("browser_handler"),
        WebSocket = require("websocket").WebSocket,
        debug = require("debug"),

        ws = new WebSocket("ws://bits.poul.org:3389"),
        handler = new Handler(browserHandler);

    debug.setLevel(3);

    ws.onmessage = function (event) {
        handler.webSocket(event);
    };

    ws.onerror = function (event) {
        debug.error("WS Error", event);
    };
});
