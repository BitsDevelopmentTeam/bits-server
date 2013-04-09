module("debug", function (require, exports) {
    "use strict";

    var console = require("console"),
        JSON = require("JSON"),

        level = 0;

    function setLevel(num) {
        level = num;
    }

    function inspect(obj) {
        if (obj !== undefined) {
            if (obj.constructor !== Object) {
                return obj.toString();
            } else {
                return JSON.stringify(obj);
            }
        }
    }

    function createLogger(prefix, num, callback) {
        return function () {
            var str = "",

                i,
                len;

            if (level >=  num) {
                str += prefix;

                for (i = 0, len = arguments.length; i < len; i += 1) {
                    str += " ";
                    str += inspect(arguments[i]);
                }
                if (console && console.log) {
                    console.log(str);
                }
            }
            if (callback !== undefined) {
                callback();
            }
        };
    }

    exports.log = createLogger("LOG:", 3);
    exports.error = createLogger("ERROR:", 2);
    exports.panic = createLogger("PANIC:", 1, function () {
        throw "Panic";
    });

    exports.setLevel = setLevel;
});
