/// <reference path="helpers/cookies.d.ts" />
"use strict"

import debug = require("debug");

export interface IEventListener extends ITemperatureHistoryEventListener, IMessageEventListener, IStatusEventListener, IConfigChangeEventListener {}

export interface IConfigChangeEventListener {
    onConfigChange():void
}

export interface ITemperatureHistoryEventListener {
    onTemperatureHistory(events: ITemperatureEvent[]):void
}

export interface IMessageEventListener {
    onMessage(event: IMessageEvent):void
}

export interface IStatusEventListener {
    onStatus(event: IStatusEvent):void
}

export interface IStatusEvent extends IEvent {
    status: Status;
    from: IUser;
}

export interface IEvent {
    when: Date;
}

export class Config {
    private blindEnabled: boolean = Cookies.get("blindEnabled") == "true";
    private static instance: Config = null;

    private constructor() {}

    static singleton(): Config {
        if (Config.instance !== null) return Config.instance;

        Config.instance = new Config();
        return Config.instance;
    }

    setBlind(val: boolean): void {
        this.blindEnabled = val;
        this.save();
    }

    getBlind(): boolean {
        return this.blindEnabled;
    }

    private save(): void {
        Cookies.set("blindEnabled", this.blindEnabled)
    }

    toString(): string {
        return "Config(blindEnabled=" + this.blindEnabled + ")";
    }
}

export enum Status { closed, open }

export interface ISensor {
    id: number;
}

export interface ITemperatureEvent extends IEvent {
    temperature: number;
    sensor: ISensor;
}

export interface IUser {
    name: string;
}

export interface IMessageEvent extends IEvent {
    content: string;
    from: IUser;
}

export class MuxEventListener implements IEventListener {
    private statusEventListeners: IStatusEventListener[] = [];
    private messageEventListeners: IMessageEventListener[] = [];
    private temperatureHistoryEventListeners: ITemperatureHistoryEventListener[] = [];
    private configChangeEventListeners: IConfigChangeEventListener[] = [];

    addListener(iel: IEventListener) {
        this.addTemperatureHistoryEventListener(iel);
        this.addConfigChangeEventListener(iel);
        this.addStatusEventListener(iel);
        this.addMessageEventListener(iel);
    }

    addMessageEventListener(mel: IMessageEventListener) {
        this.messageEventListeners.push(mel);
    }

    addStatusEventListener(sel: IStatusEventListener) {
        this.statusEventListeners.push(sel);
    }

    addTemperatureHistoryEventListener(ithe: ITemperatureHistoryEventListener) {
        this.temperatureHistoryEventListeners.push(ithe);
    }

    addConfigChangeEventListener(ccel: IConfigChangeEventListener) {
        this.configChangeEventListeners.push(ccel);
    }

    onTemperatureHistory(temps: ITemperatureEvent[]):void {
        debug.logger.log("New event: ", temps);
        for (var i = 0, len = this.temperatureHistoryEventListeners.length; i < len; i++) {
            this.temperatureHistoryEventListeners[i].onTemperatureHistory(temps);
        }
    }

    onMessage(msg: IMessageEvent):void {
        debug.logger.log("New event: ", msg);
        for (var i = 0, len = this.messageEventListeners.length; i < len; i++) {
            this.messageEventListeners[i].onMessage(msg);
        }
    }

    onStatus(s: IStatusEvent):void {
        debug.logger.log("New event: ", s);
        for (var i = 0, len = this.statusEventListeners.length; i < len; i++) {
            this.statusEventListeners[i].onStatus(s);
        }
    }

    onConfigChange():void {
        debug.logger.log("New config: ", Config.singleton());
        for (var i = 0, len = this.configChangeEventListeners.length; i < len; i++) {
            this.configChangeEventListeners[i].onConfigChange();
        }
    }
}