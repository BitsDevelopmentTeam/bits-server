module("websocket", function (require, exports) {
    "use strict";

    var WebSocket = require("WebSocket"),
        MozWebSocket = require("MozWebSocket"),
        XHR = require("XMLHttpRequest"),
        nav = require("navigator"),

        ua = nav.userAgent,

        FakeWebSocket;

    // Implements a WS fallback via XHR
    FakeWebSocket = function () {
        var fakeUrl = "http://bits.poul.org/data",
            xhr = new XHR(),
            i = 0,
            self = this;

        xhr.open("GET", fakeUrl, true);
        xhr.onreadystatechange = function handler() {
            if (self.onmessage !== undefined) {
                if (xhr.readyState === 4) {
                    self.onmessage({data: xhr.responseText});
                }
            } else {
                i += 1;
                setTimeout(function () {
                    handler();
                }, 100 * i);
            }
        };
        xhr.send(null);
    };

    function isChrome() {
        return ua.indexOf("Chrome") !== -1;
    }

    function isSafari() {
        return ua.indexOf("AppleWebKit") !== -1;
    }

    if (isSafari() && !isChrome()) { // Then WebSocket implementation is broken
        exports.WebSocket = FakeWebSocket;
    }

    exports.WebSocket = exports.WebSocket || WebSocket || MozWebSocket || FakeWebSocket;
});
