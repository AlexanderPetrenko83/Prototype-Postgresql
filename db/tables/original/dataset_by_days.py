from sqlalchemy.schema import Column
from sqlalchemy.types import String, Float, Date
from configuration.constants import DataTables
from db.bases.original_base import Base
from db.tables.original.version_loading import VersionID
from db.tables.additional_column.creation_time import CreationTime


class DatasetByDays(VersionID,
                    CreationTime,
                    DataTables,
                    Base):
    __tablename__ = DataTables.dataset_by_days

    short_name = Column(String, primary_key=True)
    unloading_point_name_rus = Column(String, primary_key=True)
    beet_shipping_day = Column(Date, primary_key=True)
    min_volume = Column(Float, nullable=False)
    max_volume = Column(Float, nullable=False)
    selected_weight = Column(Float, nullable=False)

    def __repr__(self):
        return (
            f'{DataTables.dataset_by_days}('
            f'short_name={self.short_name}, '
            f'unloading_point_name_rus={self.unloading_point_name_rus}, '
            f'beet_shipping_day={self.beet_shipping_day}, '
            f'min_volume={self.min_volume}, '
            f'max_volume={self.max_volume}, '
            f'selected_weight={self.selected_weight})'
        )
