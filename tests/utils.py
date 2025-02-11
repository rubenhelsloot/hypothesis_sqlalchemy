from sqlalchemy import Table

from hypothesis_sqlalchemy.hints import RecordType

try:
    from hypothesis.strategies import DataObject
except ImportError:
    from hypothesis._strategies import DataObject

DataObject = DataObject


def table_record_is_valid(table_record: RecordType,
                          *,
                          table: Table) -> bool:
    return all(coordinate is None
               and column.nullable
               or isinstance(coordinate, column.type.python_type)
               for coordinate, column in zip(table_record, table.columns))
