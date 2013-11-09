import mm = require("modelmapper");
import model = require("model");
import debug = require("debug");

export class Controller {
    private mux = new MuxEventListener();

    register(listener: model.IEventListener) {
        this.mux.addListener(listener);
    }

    handleUpdate(dict: any) {
        if (dict.status !== undefined) {
            this.mux.status(mm.StatusEvent.create(dict.status));
        }

        if (dict.tempint !== undefined) {
            this.mux.temperature(mm.TemperatureEvent.create(dict.tempint));
        }

        if (dict.message !== undefined) {
            this.mux.message(mm.MessageEvent.create(dict.message));
        }

        if (dict.tempinthist !== undefined) {
            this.mux.temperatureHistory(mm.ArrayTemperatureEvent.create(dict.tempinthist));
        }
    }
}

class MuxEventListener implements model.IEventListener {
    handlers: model.IEventListener[] = [];

    addListener(listener: model.IEventListener) {
        this.handlers.push(listener);
    }

    temperature(temp: model.ITemperatureEvent) {
        debug.logger.log("New event: ", temp);
        for (var i = 0, len = this.handlers.length; i < len; i++) {
            this.handlers[i].temperature(temp);
        }
    }

    temperatureHistory(temps: model.ITemperatureEvent[]) {
        debug.logger.log("New event: ", temps);
        for (var i = 0, len = this.handlers.length; i < len; i++) {
            this.handlers[i].temperatureHistory(temps);
        }
    }

    message(msg: model.IMessageEvent) {
        debug.logger.log("New event: ", msg);
        for (var i = 0, len = this.handlers.length; i < len; i++) {
            this.handlers[i].message(msg);
        }
    }

    status(s: model.IStatusEvent) {
        debug.logger.log("New event: ", s);
        for (var i = 0, len = this.handlers.length; i < len; i++) {
            this.handlers[i].status(s);
        }
    }
}