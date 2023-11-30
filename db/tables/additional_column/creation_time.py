from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func


class CreationTime(object):
    creation_time = Column(DateTime,
                           nullable=False,
                           default=func.now())
