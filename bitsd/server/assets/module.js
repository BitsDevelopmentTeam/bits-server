(function (exports) {
    "use strict";

    var modules = {}, domready = false,
        functions_buffer = [];

    function require(module_name) {
        return modules[module_name] || exports[module_name] || undefined;
    }

    function module(name, callback) {
        modules[name] = modules[name] || {};
        callback(require, modules[name]);
    }

    function loadPage() {
        if (domready === false) {
            var i = 0, len = functions_buffer.length;
            while (i < len) {
                functions_buffer[i](require);
                i += 1;
            }
            domready = true;
        }
    }

    function main(callback) {
        if (domready === false) {
            functions_buffer[functions_buffer.length] = callback;
        } else {
            callback(require);
        }
    }

    if (exports.addEventListener !== undefined) {
        exports.addEventListener("DOMContentLoded", loadPage, false);
        exports.addEventListener("load", loadPage, false);
    } else if (exports.attachEvent !== undefined) {
        exports.attachEvent("onload", loadPage);
    } else {
        exports.onload = loadPage;
    }

    exports.module = module;
    exports.main = main;
}(this));
