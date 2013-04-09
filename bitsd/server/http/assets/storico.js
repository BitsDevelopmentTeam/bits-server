module("storico", function (require, exports) {
    "use strict";

    var XHR = require("XMLHttpRequest"),
        url = "storico.php?type=JSON&page=";
    
    function setUrl(new_url) {
        url = new_url;
    }
    
    exports.setUrl = setUrl;

    function page(num, callback) {
        var xhr = new XHR();
        xhr.open("GET", url + num, true);
        xhr.onreadystatechange = function handler() {
            if (xhr.readyState === 4) {
                callback(xhr.responseText);
            }
        }
        xhr.send(null);
    }

    exports.page = page;
});
