#
# Copyright (C) 2013 Stefano Sanfilippo
# Copyright (C) 2013 BITS development team
#
# This file is part of bitsd, which is released under the terms of
# GNU GPLv3. See COPYING at top level for more information.
#

from .model import TemperatureSample, Status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


ENGINE = create_engine(dburi, echo=True)
Session = sessionmaker(bind=DBAdapter.ENGINE)

def persist(data):
    """Persist data to configured DB."""
    session = self.Session()
    session.add(data)
    session.commit()
