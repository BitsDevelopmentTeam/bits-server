/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/Chart.d.ts" />
"use strict"

import model = require("model");
import c = require("controller");
import debug = require("debug");

class Component {
    constructor(public $ctx: ZeptoCollection) {}
}

class MainComponent extends Component implements model.IConfigChangeEventListener {
    constructor($ctx: ZeptoCollection) {
        super($ctx);
        if (model.Config.singleton().getBlind()) {
            this.$ctx.addClass("blind");
        }
    }

    onConfigChange():void {
        if (model.Config.singleton().getBlind()) {
            this.$ctx.addClass("blind");
        } else {
            this.$ctx.removeClass("blind");
        }
    }
}

class TemperatureComponent extends Component implements model.ITemperatureHistoryEventListener {
    private $value = this.$ctx.find('.value');
    private $trend = this.$ctx.find('.trend');

    private trend: Trend = null;

    private onTemperature(te: model.ITemperatureEvent) {
        if (this.trend === null)
            this.trend = new Trend(te.temperature);
        this.trend.add(te.temperature);

        this.$ctx.show();

        this.$value.text(te.temperature.toPrecision(3) + "°C");
        this.$trend.text(this.trend.toString());
        this.$ctx.attr("class", te.temperature > 20 ? "high" : "low");
    }

    onTemperatureHistory(temps:model.ITemperatureEvent[]) {
        this.onTemperature(temps[temps.length - 1]);
    }
}

class TemperatureChartComponent extends Component implements model.ITemperatureHistoryEventListener {
    private chart = new TemperatureChart(this.$ctx);
    private temperatures: model.ITemperatureEvent[] = [];
    private MAXTEMP: number = 100;

    onTemperatureHistory(events:model.ITemperatureEvent[]):void {
        this.$ctx.show();

        if (events.length + this.temperatures.length > this.MAXTEMP) {
            for (var i = 0, len = (this.temperatures.length + events.length) % this.MAXTEMP; i < len; i++) {
                this.temperatures.shift();
            }
        }

        for (var i = 0, len = events.length; i < len; i++) {
            this.temperatures.push(events[i]);
        }

        this.chart.render(this.temperatures);
    }
}

class StatusComponent extends Component implements model.IStatusEventListener {
    private $value = this.$ctx.find('.value');
    private $timestamp = this.$ctx.find('.timestamp');
    private $modifiedBy = this.$ctx.find('.modified_by');

    onStatus(event:model.IStatusEvent):void {
        this.$ctx.show();
        this.$value.attr("class", model.Status[event.status] + " value");
        this.$modifiedBy.text(event.from.name);
        this.$timestamp.text(DateUtils.simple(event.when));
    }
}

class MessageComponent extends Component implements model.IMessageEventListener {
    private $user = this.$ctx.find('.user');
    private $timestamp = this.$ctx.find('.timestamp');
    private $value = this.$ctx.find('.value');

    onMessage(event:model.IMessageEvent):void {
        this.$ctx.show();
        this.$user.text(event.from.name);
        this.$value.text(event.content);
        this.$timestamp.text(DateUtils.simple(event.when));
    }
}

class TitleComponent extends Component implements model.IStatusEventListener {
    private initTitle: string = document.title;

    onStatus(event: model.IStatusEvent) {
        this.$ctx.attr("href", "/static/" + model.Status[event.status] + ".ico");
        document.title = this.capitalize(model.Status[event.status]) + " " + this.initTitle;
    }

    private capitalize(str: string) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

class HistoryBodyComponent extends Component implements model.IStatusEventListener {
    private firstStatus = true;

    onStatus(event: model.IStatusEvent) {
        if (this.endsWith(document.URL, "/log") || this.endsWith(document.URL, "/log?offset=0")) {
            if (!this.firstStatus) {
                var $status = $("<li>");
                $status.addClass(model.Status[event.status]);
                $status.text(DateUtils.simple(event.when));
                this.$ctx.prepend($status);
                this.$ctx.find("li").last().remove();
            } else {
                this.firstStatus = false;
            }
        }
    }

    private endsWith(str: string, suffix: string): boolean {
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    }
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
        c.mux.addConfigChangeEventListener(new MainComponent($('html')));
        c.mux.addStatusEventListener(new TitleComponent($('[rel="icon"]')));
    }

    static create(): UI {
        return new MainUI();
    }
}

export class IndexUI extends MainUI {
    init(c:c.Controller): void {
        super.init(c);
        c.mux.addTemperatureHistoryEventListener(new TemperatureComponent($('#temp')));
        c.mux.addTemperatureHistoryEventListener(new TemperatureChartComponent($("#temperature_graph")));
        c.mux.addMessageEventListener(new MessageComponent($('#last.msg')));
        c.mux.addStatusEventListener(new StatusComponent($('#sede')));
    }

    static create(): UI {
        return new IndexUI();
    }
}

export class HistoryUI extends MainUI {
    init(c:c.Controller): void {
        super.init(c);
        c.mux.addStatusEventListener(new HistoryBodyComponent($("ul.status")));
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