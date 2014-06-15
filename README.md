What's BITS server?
===================

BITS server is a real time presence server originally developed at
[POuL](http://www.poul.org) to let people know when to come and discuss
FOSS, get assistance or simply make friends.

Processed information is made available both in human readable HTML
and machine friendly JSON and it is consumed via a large variety of clients:
web browsers, native mobile apps, browser plugins, desktop widgets...

Note
----
Most of the URLs in this page refer to a running instance of BITS server, so they
will not work when viewing this document on GitHub (and should not, since
BITS server is not installed yet).


Architecture overview
=====================

BITS server is completed by two hardware components, forming the 3-tier
BITS architecture:

1. A STm32 ARM Cortex board connected to an LCD display for messages/
   temperature/presence updates, a button for signaling open/closed statuses
   and various environmental sensors.
2. A Fonera bridging STm32 to the server via I2C (cortex-fonera)
   and a VPN (fonera-server). The VPN setup was necessary to let BITS work
   on our campus wifi link, which is heavily filtered.
3. A web server (this!) receiving update commands via BITS-protocol,
   as detailed in the docs, and displaying public data to web clients in pull
   or push mode (true realtime).

The Cortex board is powered by Miosix OS and a daemon, both written
by that crazy genius of beta4 together with the C++ BITS developer team.
Find the code on [GitHub](https://github.com/Otacon22/bits).


This web server
===============

BITS server is written in Python and is built on Tornado. It was created with a few
objectives in mind:

1. Handling requests via events (epoll on Linux) in a single process, instead of
   forking instances, to leverage server load and work efficiently on single
   core machines -- like our current server host.
2. Handling the mighty c10k storm (and, in general, several long polling connections).
3. Serving dynamic data with minimum overhead and bandwidth consumption.
4. Enabling real time presence notifications via Web Socket push (and gracefully
   falling back to AJAX pull on older browsers).
5. Being as modular as possible.

Point _5_ is the actual reason why this project was started, as the legacy
architecture had grown around a (very smart, to say all) kludge and was deemed
to be unmaintainable.

Actually, BITS server is composed by three components:

Web Server
----------

Serving five page models:

1. [Homepage](/), which is just a skeleton: data retrieval is handled client side.
2. A [paginated history](/log), displaying information logged in the DB.
3. A mini wiki engine based on markdown. Actually, this README is rendered as the
   [info page](/info) and more informative pages are to come.
4. [Recent data](/data), in a machine parseable form (JSON).
5. [Status](/status) as a single digit (0=closed, 1=open), for building a minimal
   desktop/mobile widget.

Information on the homepage includes **presence status** (e.g. when it was
opened or closed), **current temperature** and plots of historical values.

Web Socket server
-----------------

Keeping a list of connected clients and broadcasting updates as soon as
they are processed.

BITS-miniprotocol server
------------------------

A raw TCP text-based protocol (detailed in the docs) allows
to send and receive data or commands to and from the Fonera.

This server is bound to a private address, so that only the VPN internal hosts
will be able to log data and change status.


TODOs
=====

Presence forecast
-----------------

Fede.tft and Otacon22 BITS developers came up with a great idea:
since the university timetables are fixed in a span of six months and most
students will come to POuL during breaks between lessons, we can forecast
presence by processing data from past few weeks.

The forecast is plot as a green to red table, each shade corresponding to
a decreasing probability of finding someone at the given time and day.

![Presence graph](/bits_presence.png)

MAC address detection
---------------------

Upon detection of a registered POuL member's MAC address, for more than a certain
amount of time, the Fonera will deduce that someone has arrived and flag the status
as open. Same for closing.


Notes
=====

External code
-------------

Assets in `BITS server/server/http/assets` have been imported from legacy project.

Some JS scripts are libraries licensed under the terms specified in the respective
files, the other JS scripts and the CSS files had been coded by
[thypon](https://github.com/thypon) for the legacy BITS project.

Appeareance
-----------

The style of html pages has been imported from the previous versions.
A restyle is pending and should be straightforward, as everything (including
those pre-2000 `|` breadcrumb bars) is rendered with some CSS3 magic.
We strove to keep markup as clean and semantic as possible.


Bootstrap your instance
=======================

TL;DR
-----

First create a Python environment with all libraries inside with:

    $ make virtualenv

Activate it with:

    $ . env/bin/activate

If this is the first time the daemon is run or if the DB has been reset, issue:

    $ ./bootstrap.py

Then start the daemon with:

    $ ./bitsd.py

When developing, you will find particurarly useful `--developer_mode` and
`--log_queries` command line options (see more below).

Requirements
------------

BITS is developed on Python 2.7. Python3k is not supported nor we look
forward to, although we will switch to it at some point in the future.

Hard dependencies are:

* **Tornado 3.0** asynchronous/non blocking web server on which BITS runs.
* **SQLAlchemy > 0.7** ORM and DB abstraction layer.
* **markdown** for rendering wiki pages.
* **passlib** a great abstraction over `crypt` for strong password hashing.
* **recaptcha** reCAPTCHA client library for protecting login form.

The following are not strictly necessary, but will enhance performance:

* **futures** nice implementation of the working queue used by the non-blocking engine. 
* **pycares** non-blocking DNS resolver.
* **virtualenv** for setting up a virtual environment.

Start a local instance for testing
----------------------------------

Before first use, you will have to load wiki pages into the database by running
the `./bootstrap.py` script.

Simply execute `./bitsd.py` from this directory and watch the log closely ;)
If not configured otherwise, a SQLite DB named `test.db` will be created.

Configuration
-------------

Most options can be configured via command line. Issue `./bitsd --help`
for a full list.

Managing users
--------------

Users can be added, removed and modified using `./usermanage.py` script:

    $ ./usermanage.py add test
    Password for `test`:

    $ ./usermanage.py delete test

    $ ./usermanage.py modify test
    New password for `test`:

Development
===========

Developer mode
--------------

Developer mode is turned on by passing the `--developer_mode` option
to `./bitsd.py`. When in DM, a few things happen:

1. Python modules are autoreloaded when a change is detected.
2. Verbose log is activated both in browser Javascript console and server.
3. Tornado is started in debug mode.

Another option useful for debugging is `--log_queries`, which does exactly that:
logs actual SQL passed to DBMS.

**You really do _not_ want** to activate these options when in production,
trust me.

GIT workflow
------------

The upstream repository has two main branches:

* **master** is the stable branch.
    1. _no branch_ shall be merged directly into `master`
    2. _only commits_ that can be pushed directly on this branch are typos
       and extremely urgent bugfixes. Anything else shall be merged in `development`
       (see below).
    3. since all changes committed to `master` are failsafe, changes can be
       merged into another branch anytime.
* **development** is the branche where (guess what?) development is carried on.
  **this code is not guaranteed to be safe for production** or even to execute.
    1. _new features_ will be developed in branches of `development`, then merged
       back when ready.
    2. _merge_ to `development` can happen as soon as the new feature is considered
       ready.
    3. when  code in `development` has been deemed stable, it can be merged into
       `master`.

Never push directly into upstream repository. Instead, fork the repo on GitHub,
develop according to the workflow above in your fork and then file a pull
request as soon as you have a changeset ready.

This way, it will be easy to track blocks of commits and features introduced.

Bugs and patches
----------------
This project is hosted on [GitHub](https://github.com/esseks/BITS server), you
are welcome to use the bug tracker, wishlist and make pull requests.
