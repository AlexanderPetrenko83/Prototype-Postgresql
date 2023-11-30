from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from configuration.constants import DataTables
from db.bases.original_base import Base
from db.tables.additional_column.creation_time import CreationTime


class VersionLoading(DataTables, CreationTime, Base):
    __tablename__ = DataTables.version_loading

    version_id = Column(DateTime,
                        default=func.current_date(),
                        primary_key=True)

    def __repr__(self):

        return (
            f'{DataTables.version_loading}('
            f'version_id={self.version_id} ,'
            f'creation_time={self.creation_time})'
        )


class VersionID(object):
    @declared_attr
    def version_id(cls):
        return Column(
            DateTime,
            ForeignKey(VersionLoading.version_id),
            primary_key=True,
            default=func.current_date()
        )

    @declared_attr
    def version_loading(cls):
        return relationship(VersionLoading)
        # return relationship(VersionLoading,
        #                     primaryjoin=lambda: VersionLoading.version_id==cls.version_id)


if __name__ == '__main__':
    testing_object = VersionLoading()
    print('stop')
