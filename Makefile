#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

docs:
	# Hacks PYTHONPATH to enable Sphinx compilation
	# even if bitsd is not installed.
	cd doc && PYTHONPATH=$$PYTHONPATH:$$(pwd)/.. make html

clean:
	rm -rf build/* dist/* MANIFEST
	make -f doc/Makefile clean

pyclean:
	find bitsd -name __pycache__ -print0 | xargs -0 rm -rf
	find bitsd -regex ".*\.pyc" -delete

source:
	python2 setup.py sdist

rpm:
	python2 setup.py bdist_rpm

virtualenv:
	virtualenv2 env
	. env/bin/activate && pip install tornado sqlalchemy markdown futures pycares passlib recaptcha
