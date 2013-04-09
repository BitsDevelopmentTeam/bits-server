#! /bin/sh
#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#
# Hacks PYTHONPATH to enable Sphinx compilation even if bitsd is not installed.
#
# Not necessary with bitsd installed.
#

cd doc
PYTHONPATH=$PYTHONPATH:$(pwd)/.. make html "$@"
