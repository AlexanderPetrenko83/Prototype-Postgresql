from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from configuration.constants import DataTables
from db.bases.original_base import Base
from db.tables.original.version_loading import VersionID
from db.tables.additional_column.creation_time import CreationTime
from etl.updating_rows import update_none_in_raw


class SF(VersionID, CreationTime, DataTables, Base):
    __tablename__ = DataTables.sf

    sf_id = Column(Integer, primary_key=True)
    short_name = Column(String, nullable=False)
    abbreviation = Column(String, nullable=False)

    @property
    def full_name(self):
        return f'{self.sf_id} {self.short_name} {self.version_id} {self.abbreviation}'

    def __repr__(self):

        return (
            f'{DataTables.sf}('
            f'sf_id={self.sf_id}, '
            f'short_name={self.short_name}, '
            f'version_id={self.version_id}, '
            f'abbreviation={self.abbreviation}, '
            f'creation_time={self.creation_time})'
        )


if __name__ == '__main__':
    SF_ID = 1
    SHORT_NAME = 'JOJO'
    ABBREVIATION = 'jj'
    testing_object = SF(**{'sf_id': SF_ID,
                           'short_name': SHORT_NAME,
                           'abbreviation': ABBREVIATION})
    testing_object = SF(sf_id=SF_ID,
                        short_name=SHORT_NAME,
                        abbreviation=ABBREVIATION)

    PATH_DB = "postgresql+psycopg2://admin:qwerty@localhost:5432/db_beet_schedule"
    update_none_in_raw(path_db=PATH_DB,
                       table=SF,
                       column=SF.abbreviation,
                       value='-')
