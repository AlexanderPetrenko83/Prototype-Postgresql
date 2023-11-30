import sqlalchemy
from sqlalchemy.engine import create_engine

from configuration.constants import DataSchemas
from configuration.credentials import load_config


def create_schemas(path, schemas,):
    engine = create_engine(path, echo=True)

    for schema in schemas:
        try:
            with engine.connect() as connection:
                result = connection.execute(sqlalchemy.schema.CreateSchema(schema))
                connection.commit()
        except sqlalchemy.exc.ProgrammingError:
            pass


if __name__ == '__main__':
    service_config = load_config()
    PATH = (f"postgresql+psycopg2://{service_config.db.user}:{service_config.db.password}"
            f"@{service_config.db.host}:{service_config.db.port}/{service_config.db.database}")
    SCHEMAS = list(DataSchemas().__dict__.values())
    create_schemas(PATH, SCHEMAS)
