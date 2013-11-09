/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/sockjs.d.ts" />

import v = require("view");
import c = require("controller");
import m = require("model");
import debug = require("debug");

$(function() {
    var controller = new c.Controller(),
        titleListener: m.IEventListener = v.TitleEventListener.create(),
        historyListener: m.IEventListener = v.HistoryEventListener.create(),
        socket = new SockJS("/data");

    debug.logger.level = $("meta[name='mode']").attr("content") || "production";

    controller.register(historyListener);
    controller.register(titleListener);

    socket.onmessage = (event) => controller.handleUpdate(event.data);

    socket.onerror = (event) => debug.logger.error("WS Error", event);
});