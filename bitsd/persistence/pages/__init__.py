#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

"""
Persistence module for wiki and informative pages.
"""

from .model import Page
from .. import query_by_attribute

def get_page(slug):
    """Get the page identified by the given slug."""
    return query_by_attribute(Page, 'slug', slug)
