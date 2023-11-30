import pandas as pd
import os
import sys

from sqlalchemy.sql import insert
from sqlalchemy.engine import create_engine

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ['PYTHONPATH'] = python_path

from configuration.credentials import load_config
from db.tables.original.dataset_by_days import DatasetByDays as Table


def preprocessing_and_loading(path_transformed: str,
                              dict_sf: str,
                              sugar_prod: str,
                              oper_stock: str,
                              strat_stock: str,
                              schedule: str,
                              path_db: str,
                              table: any
                              ):
    print()
    print('Preprocessing dataset by days')

    print(f'Opening {path_transformed}{dict_sf}.csv')
    df_dict_sf = (pd
                  .read_csv(f"{path_transformed}{dict_sf}.csv")
                  .drop(columns=['Unnamed: 0']))

    print(f'Opening {path_transformed}{sugar_prod}.csv')
    df_sugar_prod = (pd
                     .read_csv(f"{path_transformed}{sugar_prod}.csv")
                     .drop(columns=['Unnamed: 0'])
                     .assign(unloading_point_name_rus='производство'))

    print(f'Opening {path_transformed}{oper_stock}.csv')
    df_oper_stock = (pd
                     .read_csv(f"{path_transformed}{oper_stock}.csv")
                     .drop(columns=['Unnamed: 0'])
                     .assign(unloading_point_name_rus='оперативный запас'))

    print(f'Opening {path_transformed}{strat_stock}.csv')
    df_strat_stock = (pd
                      .read_csv(f"{path_transformed}{strat_stock}.csv")
                      .drop(columns=['Unnamed: 0'])
                      .assign(unloading_point_name_rus='стратегический запас'))

    print(f'Opening {path_transformed}{schedule}.csv')
    df_schedule = pd.read_csv(f"{path_transformed}{schedule}.csv").drop(columns=['Unnamed: 0'])

    print('Preparing dataset')
    df_dataset = pd.concat([
        df_sugar_prod,
        df_oper_stock,
        df_strat_stock
    ], ignore_index=True)

    df_dataset = df_dataset.merge(df_dict_sf, on=['sf_id'], how='left').drop(columns=['sf_id'])

    df_temp = (df_schedule
               .rename(columns={'beet_harvest_weight_selected': 'selected_weight'})
               [['beet_shipping_day', 'short_name', 'unloading_point_name_rus', 'selected_weight']]
               .groupby(['beet_shipping_day', 'short_name', 'unloading_point_name_rus'])
               [['selected_weight']]
               .sum()
               .reset_index())

    df_dataset = (df_dataset
                  .merge(df_temp,
                         on=['beet_shipping_day', 'short_name', 'unloading_point_name_rus'],
                         how='left')
                  .fillna(0)
                  [['short_name',
                    'unloading_point_name_rus',
                    'beet_shipping_day',
                    'min_volume',
                    'max_volume',
                    'selected_weight']]
                  .reset_index(drop=True)
                  .sort_values(by=['short_name', 'beet_shipping_day'], ignore_index=True))

    list_of_dicts = df_dataset.to_dict(orient='records')
    engine = create_engine(path_db, echo=False)
    print(f'Loading data to: {engine.url} {table.__table__.schema}.{table.__table__.name}')

    insert_ = insert(table).values(list_of_dicts)
    with engine.begin() as connection:
        connection.execute(insert_)

    print()


if __name__ == '__main__':
    PATH_TRANSFORMED = 'data/transformed/'
    ConfigServices = load_config()
    PATH_DB = ConfigServices.db.global_path
    DICT_SF = 'dict_sf'
    SUGAR_PROD = 'sugar_prod_constraints_by_days'
    OPER_STOCK = 'oper_stock_constraints_by_days'
    STRAT_STOCK = 'strat_stock_constraints_by_days'
    SCHEDULE = 'schedule_by_days'
    preprocessing_and_loading(PATH_TRANSFORMED,
                              DICT_SF,
                              SUGAR_PROD,
                              OPER_STOCK,
                              STRAT_STOCK,
                              SCHEDULE,
                              PATH_DB,
                              Table)
