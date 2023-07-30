# coding=utf-8
"""
Module of SqlCte class.
"""

__author__ = 'https://github.com/akvilary'

import uuid
from typing import Optional

from .sql_query import SqlQuery
from .sql_container import SqlContainer


class SqlCte:
    """
    SqlCte class is invented for better experience with filling cte queries.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """
    def __init__(
        self,
        *,
        sql_id: Optional[str | uuid.UUID] = '',
    ):
        self.ctes = {}
        self.sql_id = sql_id

    def __bool__(self) -> bool:
        return bool(self.ctes)

    def __len__(self) -> int:
        return len(self.ctes)

    def __getitem__(self, cte_name: str) -> SqlQuery:
        return self.ctes[cte_name]

    def __setitem__(self, cte_name: str, query: SqlQuery):
        self.ctes[cte_name] = query

    def __call__(self) -> SqlContainer:
        result = SqlQuery(sql_id=self.sql_id) if self.sql_id else SqlQuery()
        counter = 0
        ctes_size = len(self.ctes)
        for cte_name, cte_query in self.ctes.items():
            if counter == 0:
                result[f'with {cte_name} as'](
                    cte_query(',' if ctes_size > (counter + 1) else '')
                )
            else:
                result[f'{cte_name} as'](cte_query('' if ctes_size == (counter + 1) else ','))
            counter += 1
        return result()

    def reg(
        self,
        cte_name: str,
        sql_query: Optional[SqlQuery] = None,
        *,
        sql_id: Optional[str| uuid.UUID] = '',  # works only if sql_query parameter is not provided
    ) -> SqlQuery:
        """Create new cte and return SqlQuery instance"""
        kwargs = {}
        if sql_id:
            kwargs['sql_id'] = sql_id
        query = sql_query or SqlQuery(**kwargs)
        self[cte_name] = query
        return query
