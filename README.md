Getting started
===============

Requirements
------------

You will need Python 3 (developed on 3.2, 3.3 is fine) installed,
Tornado 2.4 and SQLAlchemy 0.7 somewhere in the Python path.

You should use virtualenv to setup a clean environment for BITS.

Start a local instance for testing
----------------------------------

Simply execute `./bitsd.sh` from this directory. Web server will be listening on
port 8008, websocket server on 3389, remote control on 8888.

Configuration
-------------

Most options can be configured via command line. Issue `bitsd.sh --help`
for a full list.

Exploring
=========

The homepage is still being setup. In the meantime, you can visit:

1. **/storico** Logging the latest 10 BITS operations.
2. **/status** A single digit, 0 means "closed", 1 means "open"
3. **/data.json** Latest data in a machine parseable flavour (no scraping ;) ).