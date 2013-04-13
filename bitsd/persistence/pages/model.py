#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from sqlalchemy import Column
from sqlalchemy.types import Text, String

import re

from .. import Base


def slugify(title):
    """Turn a title into a HTTP-friendly slug: lowercase, all
    non-letters are replaced by a dash."""
    # TODO test regex
    # Strip will remove trailing '-'
    return re.sub('[^\w]+', '-', title).strip('-').lower()


class Page(Base):
    __tablename__ = 'Pages'

    slug = Column(String(length=100), primary_key=True)
    title = Column(String(length=100), nullable=False)
    body = Column(Text, nullable=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.slug = slugify(title)

    def __str__(self):
        return 'Page: {.title}'.format(self)

    def jsondict(self):
        return {
            "title": self.title,
            "body": self.body,
            "slug": self.slug
        }
