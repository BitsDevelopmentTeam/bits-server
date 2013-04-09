module("handler", function (require, exports) {
    "use strict";

    var debug = require("debug");

    function Handler(diffHandler) {
        this.data = "";
        this.diffHandler = diffHandler;
        this.firstHandle = true;
    }

    Handler.prototype.webSocket = function (event) {
        debug.log("Incoming data", event.data);
        this.data = Handler.escapeHTML(event.data);
        this.handle();
    };

    Handler.prototype.handle = function () {
        this.jsonHandler();
    };

    Handler.prototype.jsonHandler = function () {
        var json = JSON.parse(this.data);
        if (json.status !== undefined) {
            debug.log("New Status", json.status);
            this.diffHandler.status(json.status, this.firstHandle);
        }

        if (json.msg !== undefined) {
            debug.log("New Msg", json.msg);
            this.diffHandler.msg(json.msg, this.firstHandle);
        }

        if (json.tempint !== undefined) {
            debug.log("New tempInt", json.tempint);
            this.diffHandler.tempInt(json.tempint, this.firstHandle);
        }

        if (json.tempinthist !== undefined) {
            debug.log("New tempIntHist", json.tempinthist);
            this.diffHandler.tempIntHist(json.tempinthist, this.firstHandle);
            this.diffHandler.tempInt(json.tempinthist[0], this.firstHandle);
        }

        if (this.firstHandle) {
            debug.log("First JSON arrived");
            this.firstHandle = false;
        }
    };

    Handler.escapeHTML = function (string) {
        return string.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    };

    exports.Handler = Handler;

});

/* You have to read the code bottom-up */
