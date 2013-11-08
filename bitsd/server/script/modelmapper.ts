import model = require("model");

class User implements model.IUser {
    name:string;

    private constructor() {}

    static create(name: string): model.IUser {
        var u = new User();
        u.name = name;
        return u;
    }

    toString() {
        return "User(name=" + name + ")";
    }
}

export class StatusEvent implements model.IStatusEvent {
    status:model.Status;
    from:model.IUser;
    when:Date;

    private constructor() {}

    static create(dict: any): model.IStatusEvent {
        var se = new StatusEvent;
        se.status = model.Status[dict.value];
        se.from = User.create(dict.modifiedby);
        se.when = MDate.create(dict.timestamp);
        return se;
    }

    toString() {
        return "StatusEvent(status= " + model.Status[this.status] + ",from=" + this.from.toString() + ",when=" + this.when.toString() + ")";
    }
}

class MDate {
    static create(rep: number): Date {
        var d = new Date(rep);
        return d;
    }
}

class Sensor implements model.ISensor {
    id:number;

    private constructor() {}

    static create(id: number) {
        var s = new Sensor();
        s.id = id;
        return s;
    }

    toString() {
        return "Sensor(id=" + this.id.toString() +")";
    }
}

export class TemperatureEvent implements model.ITemperatureEvent {
    temperature:number;
    when:Date;
    sensor:model.ISensor;

    private constructor() {}

    static create(dict: any) {
        var te = new TemperatureEvent();
        te.temperature = dict.value;
        te.when = MDate.create(dict.timestamp);
        te.sensor = Sensor.create(dict.sensor);
        return te;
    }

   toString() {
        return "TemperatureEvent(temperature= " + this.temperature.toString() + ",sensor=" + this.sensor.toString() + ",when=" + this.when.toString() + ")";
   }
}

export class ArrayTemperatureEvent {
    private constructor() {}

    static create(dict: any[]): TemperatureEvent[] {
        var tes: TemperatureEvent[] = [];

        for (var i = 0, len = dict.length; i < len; i++) {
            tes.unshift(TemperatureEvent.create(dict[i]))
        }

        return tes;
    }
}

export class MessageEvent implements model.IMessageEvent {
    when:Date;
    content:string;
    from:model.IUser;

    private constructor() {}

    static create(dict: any): model.IMessageEvent {
        var me = new MessageEvent();
        me.content = dict.value;
        me.from = User.create(dict.user);
        me.when = MDate.create(dict.timestamp);
        return me;
    }

    toString() {
        return "MessageEvent(from= " + this.from.toString() + ",content=" + this.content.toString() + ",when=" + this.when.toString() + ")";
    }
}