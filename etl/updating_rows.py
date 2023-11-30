from sqlalchemy.engine import create_engine
from sqlalchemy.sql import update

# from tables.table_description.original.sf import SF


def update_none_in_raw(path_db: str,
                       table: object,
                       column: object,
                       value: any):
    engine = create_engine(path_db, echo=True)

    upd = update(table).where(column == None).values(abbreviation=value)
    with engine.connect() as connection:
        result = connection.execute(upd)
        connection.commit()


if __name__ == '__main__':
    PATH_DB = "postgresql+psycopg2://admin:qwerty@localhost:5432/db_beet_schedule"
    # update_none_in_raw(path_db=PATH_DB,
    #                    table=SF,
    #                    column=SF.abbreviation,
    #                    value='-')
