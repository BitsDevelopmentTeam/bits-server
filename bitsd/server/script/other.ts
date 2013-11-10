/// <reference path="helpers/zepto.d.ts" />
"use strict"

import v = require("view");
import c = require("controller");

$(function() {
    var controller = new c.Controller();
    v.MainUI.create().init(controller);
});