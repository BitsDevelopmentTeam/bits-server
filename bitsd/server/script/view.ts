/// <reference path="helpers/zepto.d.ts" />
/// <reference path="helpers/Chart.d.ts" />

import model = require("model");
import debug = require("debug");

export class IndexEventListener implements model.IEventListener {
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
    private temperatures: model.ITemperatureEvent[] = null;

    temperature(te: model.ITemperatureEvent) {
        if (this.trend === null)
            this.trend = new Trend(te.temperature);
        this.trend.add(te.temperature);

        this.$temperature.show();

        this.$temperatureValue.text(te.temperature.toPrecision(3) + "°C");
        this.$temperatureTrend.text(this.trend.toString());
        this.$temperature.attr("class", te.temperature > 20 ? "high" : "low");

        if (this.temperatures !== null) {
            this.temperatures.shift();
            this.temperatures.push(te);
            this.chart.render(this.temperatures);
        }
    }

    temperatureHistory(temps:model.ITemperatureEvent[]) {
        this.$chart.show();
        this.temperatures = temps;
        this.temperatures.pop();
        this.chart.render(this.temperatures);
    }

    message(msg:model.IMessageEvent) {
        this.$message.show();
        this.$messageUser.text(msg.from.name);
        this.$messageValue.text(msg.content);
        this.$messageTimestamp.text(DateUtils.simple(msg.when));
    }

    status(s:model.IStatusEvent) {
        this.$status.show();
        this.$statusValue.attr("class", model.Status[s.status] + " value");
        this.$statusModifiedBy.text(s.from.name);
        this.$statusTimestamp.text(DateUtils.simple(s.when));
    }

    static create(): model.IEventListener {
        return new IndexEventListener();
    }
}

export class TitleEventListener implements model.IEventListener {
    private $favicon = $('[rel="icon"]');
    private initTitle: string = document.title;

    temperature(event: model.ITemperatureEvent) {}

    temperatureHistory(events: model.ITemperatureEvent[]) {}

    message(event: model.IMessageEvent) {}

    status(event: model.IStatusEvent) {
        this.$favicon.attr("href", "/static/" + model.Status[event.status] + ".ico");
        document.title = this.capitalize(model.Status[event.status]) + " " + this.initTitle;
    }

    private capitalize(str: string) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    static create(): model.IEventListener {
        return new TitleEventListener();
    }
}

export class HistoryEventListener implements model.IEventListener {
    private firstStatus = true;
    private $stata = $("ul.status");

    temperature(event: model.ITemperatureEvent) {}

    temperatureHistory(events: model.ITemperatureEvent[]) {}

    message(event: model.IMessageEvent) {}

    status(event: model.IStatusEvent) {
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

    static create(): model.IEventListener {
        return new HistoryEventListener();
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

            l.push(date.getHours().toString() + ":" + date.getMinutes().toString());
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

class Trend {
    diff: number = 0;

    constructor(public oldValue: number) {}

    add(value) {
        this.diff = value - this.oldValue;
        this.oldValue = value;
        debug.logger.log("The difference between the current temp and the old temp is", this.diff);
    }

    toString() {
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
        return date.getFullYear() + "-" + date.getMonth() + "-" + date.getDay() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
    }
}