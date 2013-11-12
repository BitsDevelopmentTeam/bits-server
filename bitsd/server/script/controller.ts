/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/sockjs.d.ts" />

"use strict"

import mm = require("modelmapper");
import model = require("model");
import debug = require("debug");

export class Controller {
    mux = new model.MuxEventListener();
    private firstTemp = true;
    private socket: SockJS = new SockJS("/data");

    constructor() {
        debug.logger.setLevel($("meta[name='mode']").attr("content") || "production");
        $("[href='#blind']").on("click", (event) => !(this.blindClicked() || true))
        this.socket.onmessage = (event) => this.handleUpdate(event.data);
    }

    private handleUpdate(dict: any) {
        if (dict.status !== undefined) {
            this.mux.onStatus(mm.StatusEvent.create(dict.status));
        }

        if (dict.tempint !== undefined) {
            if (!this.firstTemp) {
                this.mux.onTemperatureHistory([mm.TemperatureEvent.create(dict.tempint)]);
            } else {
                this.firstTemp = false;
            }
        }

        if (dict.message !== undefined) {
            this.mux.onMessage(mm.MessageEvent.create(dict.message));
        }

        if (dict.tempinthist !== undefined) {
            this.mux.onTemperatureHistory(mm.ArrayTemperatureEvent.create(dict.tempinthist));
        }
    }

    private blindClicked(): boolean {
        var config = model.Config.singleton();
        config.setBlind(!config.getBlind());
        this.mux.onConfigChange();
        return true;
    }
}