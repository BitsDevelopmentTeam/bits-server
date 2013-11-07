/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/window.extend.d.ts" />

class FakeWebSocket {
    public onmessage: Function;

    constructor() {
        var self = this;
        $.get("/data", function(response) {
            if (self.onmessage != undefined) {
                self.onmessage({data: response})
            }
        });
    }
}

export var Socket = WebSocket || MozWebSocket || FakeWebSocket;