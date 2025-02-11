from typing import Optional

from hypothesis.searchstrategy.collections import TupleStrategy
from sqlalchemy import Table

from hypothesis_sqlalchemy import columnar
from hypothesis_sqlalchemy.hints import Strategy


def factory(table: Table,
            **fixed_columns_values: Strategy) -> TupleStrategy:
    return columnar.records.factory(table.columns,
                                    **fixed_columns_values)


def lists_factory(table: Table,
                  *,
                  min_size: int = 0,
                  max_size: Optional[int] = None,
                  **fixed_columns_values: Strategy) -> TupleStrategy:
    return columnar.records.lists_factory(table.columns,
                                          min_size=min_size,
                                          max_size=max_size,
                                          **fixed_columns_values)
