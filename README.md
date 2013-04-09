Getting started
===============

Requirements
------------

You will need **Python 3** (developed on 3.2, 3.3 is fine) installed,
**Tornado 2.4** and **SQLAlchemy 0.7** (but 0.8 should be fine)
somewhere in the Python path.

You should use virtualenv to setup a clean environment for BITS.

Start a local instance for testing
----------------------------------

Simply execute `./bitsd.py` from this directory and watch the log closely ;)

Configuration
-------------

Most options can be configured via command line. Issue `bitsd.py --help`
for a full list.

Docs
====

**NOTE**: We use Sphinx autodiscovery to generate docs. If you don't have bitsd
in `PYTHONPATH` env variable, please use `./makedocs.sh` instead of
`doc/Makefile` to set it up.