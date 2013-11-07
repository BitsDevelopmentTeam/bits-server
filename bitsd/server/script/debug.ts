export interface ILogger {
    level: string;
    log(...args);
    error(...args);
    panic(...args);
}

class Logger implements ILogger {
    private levels: string[];
    private levelId: number = 0;

    constructor(...args: string[]) {
        this.levels = args;
    }

    set level(l: string) {
        this.levelId = this.levels.indexOf(l);
    }

    get level(): string {
        return this.levels[this.levelId];
    }

    private stringrep(obj): string {
        if (obj !== undefined) {
            if (obj.constructor !== Object) {
                return obj.toString();
            } else {
                return JSON.stringify(obj);
            }
        } else {
            return "";
        }
    }

    log(...args) {
        var str = "LOG:";

        if (this.levelId >=  2) {

            for (var i = 0, len = args.length; i < len; i += 1) {
                str += " ";
                str += this.stringrep(args[i]);
            }
            if (console && console.log) {
                console.log(str);
            }
        }
    }

    error(...args) {
        var str = "DEBUG:";

        if (this.levelId >=  1) {

            for (var i = 0, len = args.length; i < len; i += 1) {
                str += " ";
                str += this.stringrep(args[i]);
            }
            if (console && console.log) {
                console.log(str);
            }
        }
    }

    panic(...args) {
        var str = "PANIC:";

        if (this.levelId >=  0) {

            for (var i = 0, len = args.length; i < len; i += 1) {
                str += " ";
                str += this.stringrep(args[i]);
            }
            if (console && console.log) {
                console.log(str);
            }
        }

        throw "RED BUTTON PRESSED, PANIC, PANIC, PANIC!!!";
    }
}

export var logger: ILogger = new Logger("production", "test", "debug");