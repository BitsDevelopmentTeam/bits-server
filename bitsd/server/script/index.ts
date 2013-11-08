/// <reference path="helpers/zepto.d.ts" />

import ws = require("websocket");
import v = require("view");
import c = require("controller");
import m = require("model");
import debug = require("debug");

$(function() {
    var controller = new c.Controller(),
        indexListener: m.IEventListener = v.IndexEventListener.create(),
        titleListener: m.IEventListener = v.TitleEventListener.create(),
        socket = new ws.Socket(/https/.test(location.protocol)? "wss": "ws" + "://" + location.hostname + ":" + location.port +"/ws");

    debug.logger.level = $("meta[name='mode']").attr("content") || "production";

    controller.register(indexListener);
    controller.register(titleListener);

    socket.onmessage = (event) => controller.handleUpdate($.parseJSON(event.data));

    socket.onerror = (event) => debug.logger.error("WS Error", event);
});