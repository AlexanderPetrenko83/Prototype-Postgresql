from dataclasses import dataclass


NAMING_CONVENTION={
        "all_column_names": lambda constraint, table: '_'.join([
            column.name for column in constraint.columns.values()
        ]),
        "ix": "ix_%(table_name)s_%(all_column_names)s",
        "uq": "uq_%(table_name)s_%(all_column_names)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(all_column_names)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


@dataclass
class DataSchemas:

    original: str = 'original'
    preprocessed: str = 'preprocessed'
    calculated: str = 'calculated'
    reported: str = 'reported'


class DataTables:

    version_loading = 'version_loading'
    sf = 'sf'
    volume = 'volume'
    report = 'report'
    checking = 'checking'
    schedule = 'schedule'
    dataset_by_days = 'dataset_by_days'


SELECTED_VERSION = '2023-11-28 00:00:00.000000'
