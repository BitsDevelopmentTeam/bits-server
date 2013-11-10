/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/Chart.d.ts" />
"use strict"

import model = require("model");
import c = require("controller");
import debug = require("debug");

class MainComponent implements model.IConfigChangeEventListener {
    $html = $("html");

    constructor() {
        if (model.Config.singleton().getBlind()) {
            this.$html.addClass("blind");
        }
    }

    onConfigChange():void {
        if (model.Config.singleton().getBlind()) {
            this.$html.addClass("blind");
        } else {
            this.$html.removeClass("blind");
        }
    }
}

class IndexBodyComponent implements model.IEventListener {
    private $temperature  = $("#temp");
    private $temperatureValue = this.$temperature.find(".value");
    private $temperatureTrend = this.$temperature.find(".trend");
    private $status = $("#sede");
    private $statusValue = this.$status.find(".value");
    private $statusTimestamp = this.$status.find(".timestamp");
    private $statusModifiedBy = this.$status.find(".modified_by");
    private $message = $("#last.msg");
    private $messageUser = this.$message.find(".user");
    private $messageTimestamp = this.$message.find(".timestamp");
    private $messageValue = this.$message.find(".value");
    private $chart = $("#temperature_graph");

    private trend: Trend = null;
    private chart = new TemperatureChart(this.$chart);
    private temperatures: model.ITemperatureEvent[] = [];

    private onTemperature(te: model.ITemperatureEvent) {
        if (this.trend === null)
            this.trend = new Trend(te.temperature);
        this.trend.add(te.temperature);

        this.$temperature.show();

        this.$temperatureValue.text(te.temperature.toPrecision(3) + "°C");
        this.$temperatureTrend.text(this.trend.toString());
        this.$temperature.attr("class", te.temperature > 20 ? "high" : "low");
    }

    onTemperatureHistory(temps:model.ITemperatureEvent[]) {
        this.$chart.show();

        for (var i = 0, len = temps.length; i < len; i++) {
            this.temperatures.shift();
        }

        for (var i = 0, len = temps.length; i < len; i++) {
            this.temperatures.push(temps[i]);
        }

        this.onTemperature(temps[i-1]);

        this.chart.render(this.temperatures);
    }

    onMessage(msg:model.IMessageEvent) {
        this.$message.show();
        this.$messageUser.text(msg.from.name);
        this.$messageValue.text(msg.content);
        this.$messageTimestamp.text(DateUtils.simple(msg.when));
    }

    onStatus(s:model.IStatusEvent) {
        this.$status.show();
        this.$statusValue.attr("class", model.Status[s.status] + " value");
        this.$statusModifiedBy.text(s.from.name);
        this.$statusTimestamp.text(DateUtils.simple(s.when));
    }

    onConfigChange():void {}
}

class TitleComponent implements model.IStatusEventListener {
    private $favicon = $('[rel="icon"]');
    private initTitle: string = document.title;

    onStatus(event: model.IStatusEvent) {
        this.$favicon.attr("href", "/static/" + model.Status[event.status] + ".ico");
        document.title = this.capitalize(model.Status[event.status]) + " " + this.initTitle;
    }

    private capitalize(str: string) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

class HistoryBodyComponent implements model.IStatusEventListener {
    private firstStatus = true;
    private $stata = $("ul.status");

    onStatus(event: model.IStatusEvent) {
        if (!this.firstStatus) {
            var $status = $("<li>");
            $status.addClass(model.Status[event.status]);
            $status.text(DateUtils.simple(event.when));
            this.$stata.prepend($status);
            this.$stata.find("li").last().remove();
        } else {
            this.firstStatus = false;
        }
    }

    onConfigChange():void {}
}

class TemperatureChart {
    ctx: any;

    constructor(elem: ZeptoCollection) {
        var canvas = <HTMLCanvasElement>elem.get()[0];
        this.ctx = canvas.getContext("2d");
    }

    render(tss: model.ITemperatureEvent[]) {
        var data = {
            labels: this.labels(tss, 7),
            datasets: [this.dataset(tss)]
        };

        new Chart(this.ctx).Line(data, {
            scaleGridLineColor : "rgba(255,255,255,.05)"
        });
    }

    private labels(tss: model.ITemperatureEvent[], num: number): string[] {
        var l: string[] = [],
            interval = Math.floor(tss.length / num),
            offset = Math.floor((tss.length % num) / 2);

        for (var i = 0; i < num; i++) {
            var date = tss[i * interval + offset].when;

            l.push(date.getHours().toString() + ":" + DateUtils.twoNums(date.getMinutes()));
        }

        return l;
    }

    private dataset(tss: model.ITemperatureEvent[]): LineDataset {
        var d: number[] = [];
        for (var i = 0, len = tss.length; i < len; i++) {
            d.push(tss[i].temperature);
        }

        return {
            fillColor : "rgba(0,255,0,0.5)",
			strokeColor : "rgba(0,255,0,1)",
			pointColor : "rgba(255,0,0,1)",
            pointStrokeColor: "#fff",
            data: d};
    }
}

export interface UI {
    init(c:c.Controller): void
}

export class MainUI implements UI {
    private constructor() {}

    init(c:c.Controller): void {
        c.mux.addConfigChangeEventListener(new MainComponent());
        c.mux.addStatusEventListener(new TitleComponent());
    }

    static create(): UI {
        return new MainUI();
    }
}

export class IndexUI extends MainUI {
    init(c:c.Controller): void {
        super.init(c);
        c.mux.addListener(new IndexBodyComponent());
    }

    static create(): UI {
        return new IndexUI();
    }
}

export class HistoryUI extends MainUI {
    init(c:c.Controller): void {
        super.init(c);
        c.mux.addStatusEventListener(new HistoryBodyComponent());
    }

    static create(): UI {
        return new HistoryUI();
    }
}

class Trend {
    diff: number = 0;

    constructor(public oldValue: number) {}

    add(value: number): void {
        this.diff = value - this.oldValue;
        this.oldValue = value;
        debug.logger.log("The difference between the current temp and the old temp is", this.diff);
    }

    toString(): string {
        if (this.diff === 0) {
            return "→";
        } else if (this.diff > 0) {
            return "↗";
        } else {
            return "↘";
        }
    }
}

class DateUtils {
    static simple(date: Date): string {
        return date.getFullYear() + "-" + date.getMonth() + "-" + date.getDay() + " " + date.getHours() + ":" + DateUtils.twoNums(date.getMinutes()) + ":" + DateUtils.twoNums(date.getSeconds());
    }

    static twoNums(num: number): string {
        if (num > 60) throw new RangeException();
        if (num < 0) throw new RangeException();

        return num > 10 ? num.toString() : "0" + num.toString();
    }
}