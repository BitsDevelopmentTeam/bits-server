How the project is structured
=============================

With the exception of `./templates`, each directory contains a specific server:

*pages* web pages server (homepage, logs, admin etc.).
*websocket* websockets (push) server. Currently, used to push Sede status.
*remote* remote control servers: send and receive commands from Fonera or Web.

Each submodule contains a specific handler (the name _should be_ meaningful).

A server is started by calling <module name>.startserver() command (see main())


Getting started
===============

Start a local instance for testing
----------------------------------

Simply execute `./bitsd.sh` from this directory. Web server will be listening on
port 8008, websocket server on 3389, remote control on 8888.