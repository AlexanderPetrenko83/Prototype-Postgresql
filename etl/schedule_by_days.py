import os
import sys

import pandas as pd

from sqlalchemy.sql import insert
from sqlalchemy.engine import create_engine

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ['PYTHONPATH'] = python_path

from configuration.credentials import load_config
from configuration.constants import SELECTED_VERSION
# from db.tables.original.schedule import Schedule as Table


def extract(path_raw: str,
            file_raw: str,
            path_extracted: str,
            file_extracted: str):
    print()
    print(f'Extracting data from: {path_raw}{file_raw}.csv')
    df = pd.read_csv(f'{path_raw}{file_raw}.csv')

    print(f'Saving data to: {path_extracted}{file_extracted}.csv')
    df.to_csv(f'{path_extracted}{file_extracted}.csv')


def transform(path_extracted: str,
              file_extracted: str,
              selected_version: str,
              path_transformed: str,
              file_transformed: str):
    print()
    print(f'Opening {path_extracted}{file_extracted}.csv')
    df = pd.read_csv(f'{path_extracted}{file_extracted}.csv')

    print('Transforming data')
    df = df.query("version_id == @selected_version")
    columns = [
        'loading_point_id',
        'loading_point_name_rus',
        'beet_harvest_day',
        'beet_shipping_day',
        'short_name',
        'unloading_point_name_rus',
        'beet_harvest_weight_selected'
    ]
    df = df[columns]

    print(f'Saving data to: {path_transformed}{file_transformed}.csv')
    df.to_csv(f'{path_transformed}{file_transformed}.csv')


def load_data(path_transformed: str,
              file_transformed: str,
              path_db: str,
              table: any):
    print()
    print(f'Opening {path_transformed}{file_transformed}.csv')
    df = pd.read_csv(f'{path_transformed}{file_transformed}.csv')

    list_of_dicts = df.to_dict(orient='records')
    engine = create_engine(path_db, echo=False)
    print(f'Loading data to: {engine.url} {table.__table__.schema}.{table.__table__.name}')

    insert_ = insert(table).values(list_of_dicts)
    with engine.begin() as connection:
        connection.execute(insert_)

    print()


if __name__ == "__main__":
    FILE_RAW = FILE_EXTRACTED = FILE_TRANSFORMED = 'schedule_by_days'
    PATH_RAW = 'data/raw/'
    PATH_EXTRACTED = 'data/extracted/'
    PATH_TRANSFORMED = 'data/transformed/'

    ConfigServices = load_config()
    PATH_DB = ConfigServices.db.global_path

    extract(PATH_RAW, FILE_RAW, PATH_EXTRACTED, FILE_EXTRACTED)
    transform(PATH_EXTRACTED, FILE_EXTRACTED, SELECTED_VERSION, PATH_TRANSFORMED, FILE_TRANSFORMED)
    # load_data(PATH_TRANSFORMED, FILE_TRANSFORMED, PATH_DB, Table)
