main(function (require) {
    "use strict";

    var Handler = require("handler").Handler,
        browserHandler = require("browser_handler"),
        WebSocket = require("websocket").WebSocket,
        location = require("location"),
        query = require("peppy").query,
        debug = require("debug"),

        ws = new WebSocket("ws://" + location.hostname + ":" + location.port + "/ws"),
        handler = new Handler(browserHandler);

    debug.setLevel(query("meta[name='mode']").content);

    ws.onmessage = function (event) {
        handler.webSocket(event);
    };

    ws.onerror = function (event) {
        debug.error("WS Error", event);
    };
});
