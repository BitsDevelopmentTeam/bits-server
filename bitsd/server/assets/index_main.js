main(function (require) {
    "use strict";

    require("location");

    var Handler = require("handler").Handler,
        browserHandler = require("browser_handler"),
        WebSocket = require("websocket").WebSocket,
        debug = require("debug"),

        ws = new WebSocket("ws://" + window.location.hostname + ":" + location.port + "/ws"),
        handler = new Handler(browserHandler);

    debug.setLevel(3);

    ws.onmessage = function (event) {
        handler.webSocket(event);
    };

    ws.onerror = function (event) {
        debug.error("WS Error", event);
    };
});
