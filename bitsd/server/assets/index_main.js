main(function (require) {
    "use strict";

    var Handler = require("handler").Handler,
        browserHandler = require("browser_handler"),
        WebSocket = require("websocket").WebSocket,
        location = require("location"),
        query = require("peppy").query,
        debug = require("debug"),

        ws = new WebSocket("wss://" + location.hostname + ":" + location.port + "/ws"),
        handler = new Handler(browserHandler);

    var debugMeta = query("meta[name='mode']")[0];
    if (debugMeta) {
        debug.setLevel(debugMeta.content);
    } else {
        debug.setLevel("production");
    }

    ws.onmessage = function (event) {
        handler.webSocket(event);
    };

    ws.onerror = function (event) {
        debug.error("WS Error", event);
    };
});
