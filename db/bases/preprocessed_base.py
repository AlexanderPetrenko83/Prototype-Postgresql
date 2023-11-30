from sqlalchemy.schema import MetaData
from sqlalchemy.orm import declarative_base
from configuration.constants import DataSchemas


metadata_obj = MetaData(schema=DataSchemas.preprocessed)
Base = declarative_base(metadata=metadata_obj)
