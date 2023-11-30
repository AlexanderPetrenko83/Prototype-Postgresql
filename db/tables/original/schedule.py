from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Date
from configuration.constants import DataTables
from db.bases.original_base import Base
from db.tables.original.version_loading import VersionID
from db.tables.additional_column.creation_time import CreationTime
from etl.updating_rows import update_none_in_raw


class Schedule(VersionID,
               CreationTime,
               DataTables,
               Base):
    __tablename__ = DataTables.schedule

    loading_point_id = Column(String, primary_key=True)
    loading_point_name_rus = Column(String, nullable=False)
    beet_harvest_day = Column(Date, primary_key=True)
    beet_shipping_day = Column(String, primary_key=True)
    short_name = Column(String, nullable=False)
    unloading_point_name_rus = Column(String, primary_key=True)
    beet_harvest_weight_selected = Column(Integer, nullable=False)

    def __repr__(self):

        return (
            f'{DataTables.schedule}('
            f'loading_point_id={self.loading_point_id}, '
            f'loading_point_name_rus={self.loading_point_name_rus}, '
            f'beet_harvest_day={self.beet_harvest_day}, '
            f'beet_shipping_day={self.beet_shipping_day}, '
            f'short_name={self.short_name}, '
            f'unloading_point_name_rus={self.unloading_point_name_rus}, '
            f'beet_harvest_weight_selected={self.beet_harvest_weight_selected})'
        )
