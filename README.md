Getting started
===============

Start a local instance for testing
----------------------------------

Simply execute `./bitsd.sh` from this directory. Web server will be listening on
port 8008, websocket server on 3389, remote control on 8888.

Configuration
-------------

Most options can be configured via command line. Issue `bitsd.sh --help`
for a full list.

How the project is structured
=============================

With the exception of `./templates`, each directory contains a specific server:

1. **pages**: web pages server (homepage, logs, admin etc.).
2. **websocket**: websockets (push) server. Currently, used to push Sede status.
3. **remote**: remote control servers: send and receive commands from Fonera or Web.

Each submodule contains a specific handler (the name _should be_ meaningful).

A server is started by calling <module name>.startserver() command (see main())
