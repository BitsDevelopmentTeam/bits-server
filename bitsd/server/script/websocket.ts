/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/window.extend.d.ts" />

class FakeWebSocket {
    public onmessage: Function = undefined;

    constructor() {
        var self = this;

        $.get("/data", (response) => self.onmessage !== undefined && self.onmessage({data: response}));
    }
}

export var Socket = WebSocket || MozWebSocket || FakeWebSocket;