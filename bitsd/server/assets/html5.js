module("html5", function (require, exports) {
    "use strict";

    var doc = require("document"),
        debug = require("debug"),
        nav = require("navigator"),
        av = nav.appVersion,
        elements = "abbr,article,aside,audio,bb,canvas,datagrid,datalist,details,dialog,eventsource,figure,footer,header,hgroup,mark,menu,meter,nav,output,progress,section,time,video".split(','),
        i = 0,
        len = elements.length;

    function isIE() {
        return av.indexOf("MSIE") !== -1;
    }

    function IEVersion() {
        return parseFloat(av.split("MSIE")[1], 10);
    }

    exports.value = isIE();
    exports.version = IEVersion();

    if (exports.value === true && exports.version === 8) {
        debug.log("The Browser is Internet Explorer version", exports.version);
        debug.log("Applying HTML5 quirks");
        while (i < len) {
            doc.createElement(elements[i]);
            i += 1;
        }
    }
});
