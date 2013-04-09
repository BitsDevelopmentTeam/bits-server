module("browser_handler", function (require, exports) {
    "use strict";

    var doc = require("document"),
        debug = require("debug"),
        query = require("peppy").query,
        Raphael = require("Raphael"),

        sede,
        sedeValue,
        sedeTimestamp,
        sedeModifiedBy,
        temp,
        tempValue,
        tempTrend,
        msg,
        msgTimestamp,
        msgUser,
        msgValue,
        head,
        title,
        favicon,
        trend,
        tempGraph,
        lastTimestamp,
        tempGraphValuesY = [],
        tempGraphTimestampValues = [],
        tempGraphHeight = 380,
        tempGraphWidth = 380;

    /* HELPERS */

    function seq(x, y) {
        var container = [];

        if (x < y) {
            while (x < y) {
                container[container.length] = x;
                x++;
            }
        } else {
            while (x < y) {
                container[container.length] = x;
                x--;
            }
        }

        return container;
    }

    // Show a DOM hidden element
    function show(elem) {
        debug.log("Showing", elem.id);
        elem.setAttribute("style", "display: block");
    }

    // Return a new string capitalized
    function capitalize(string) {
        debug.log("Capitilizing string", string);
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Change the favicon icon of the site.
    function changeIcon(status) {
        debug.log("Changing favicon", status);
        var link = doc.createElement("link");
        head.removeChild(favicon);
        link.href = "img/" + status + ".ico";
        link.rel = "shortcut icon";
        head.appendChild(link);
        favicon = link;
    }

    // the Trend object contains an old state off the value defined
    //  - newValue
    //      add a new state to the _oldValue_  state and 
    //      assign the difference between the new state and the
    //      old value to the _diff_ state.
    //
    //  - toString
    //      Respond to the toString message, transorm the object in an intelligible form.
    //      In this case the trend arcs.
    function Trend() {
        debug.log("New Trend Object instanziated");
        this.oldValue = undefined;
        this.diff = 0;
    }

    Trend.prototype.newValue = function (value) {
        if (this.oldValue !== undefined) {
            this.diff = value - this.oldValue;
            debug.log("The difference between the current temp and the old temp is", this.diff);
        }
        debug.log("The value of the oldTemp is now", value);
        this.oldValue = value;

        return this;
    };

    Trend.prototype.toString = function () {
        if (this.diff === 0) {
            return "→";
        } else if (this.diff > 0) {
            return "↗";
        } else {
            return "↘";
        }
    };

    function swith(elem, callback) {
        if (elem !== undefined) {
            debug.log(elem, "selected");
            if (callback !== undefined) {
                callback();
            }
        } else {
            debug.error(elem, "not selectable");
        }
    }

    /* END HELPERS */


    /* DOM Selecting initialization */
    main(function () {
        sede = doc.getElementById("sede");
        swith(sede, function () {
            sedeValue = query(".value", sede)[0];
            sedeTimestamp = query(".timestamp", sede)[0];
            sedeModifiedBy = query(".modified_by", sede)[0];
        });

        temp = doc.getElementById("temp");
        swith(temp, function () {
            tempValue = query(".value", temp)[0];
            tempTrend = query(".trend", temp)[0];
        });

        msg = query("#last.msg")[0];
        swith(msg, function () {
            msgUser = query(".user", msg)[0];
            msgTimestamp = query(".timestamp", msg)[0];
            msgValue = query(".value", msg)[0];
        });

        title = doc.title;
        swith(title);

        favicon = query('[rel="icon"]')[0];
        swith(favicon);

        head = doc.head || doc.getElementsByTagName('head')[0];
        swith(head);

        tempGraph = Raphael("temperature_graph", tempGraphWidth, tempGraphHeight);

        trend = new Trend();
    });

    /* Handler functions definition */
    // Handle BITS status change.
    function statusHandler(status, first) {
        debug.log("browserHandler handling status");
        if (first) {
            show(sede);
        }
        var value = status.value === "open" ? "open" : "close";
        changeIcon(value);
        doc.title = capitalize(value) + " " + title;
        sedeValue.setAttribute("class", value + " value");
        sedeTimestamp.innerHTML = status.timestamp;
        sedeModifiedBy.innerHTML = status.modifiedby;
    }

    // Handle MSGs arrival (somewhere in the future)
    function msgHandler(msg, first) {
        debug.log("MSG arrived but there isn't an handler");
        /* pass
        if(first) show(msg);
        msgUser.innerHTML = msg.user;
        msgTimestamp.innerHTML = msg.timestamp;
        msgValue.innerHTML = msg.value;
        */
    }

    // Handle tempInt arrival
    function tempIntHandler(tempInt, first) {
        debug.log("browserHandler handling tempint");

        if (first) {
            show(temp);
        }
        tempValue.innerHTML = tempInt.value.toPrecision() + "°C";

        if (lastTimestamp !== tempInt.timestamp) {
            tempTrend.innerHTML = trend.newValue(tempInt.value);
            if (!first) {
                tempGraph.addTemp(tempInt);
            }
        }
        temp.setAttribute("class", tempInt.value > 20 ? "high" : "low");
    }

    
    function tempIntHistHandler(tempIntHist, first) {
        debug.log("browserHandler handling tempIntHist");
        var cordX = 0,
            cordY = 0,
            reversedHistory = tempIntHist.reverse();

        for (var i = 0; i < tempIntHist.length; i++) {
            tempGraphValuesY[tempGraphValuesY.length] = tempIntHist[i].value;
            tempGraphTimestampValues[tempGraphTimestampValues.length] = tempIntHist[i].timestamp;
        }

        tempGraph.linechart(
            cordX, cordY,
            tempGraphHeight, tempGraphWidth,
            seq(0, tempGraphValuesY.length), tempGraphValuesY,
            {
                shade: true,
                colors: ["#0F0"]
            }
        );
    }

    // Exports only the browserHandler object in the global scope
    exports.status = statusHandler;
    exports.msg = msgHandler;
    exports.tempInt = tempIntHandler;
    exports.tempIntHist = tempIntHistHandler;
});