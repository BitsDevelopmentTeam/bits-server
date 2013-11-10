/// <reference path="helpers/zepto.d.ts" />
"use strict"

import v = require("view");
import c = require("controller");
import m = require("model");

$(function() {
    var controller = new c.Controller();
    v.MainUI.create().init(controller);
});