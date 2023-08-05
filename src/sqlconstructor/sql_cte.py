# coding=utf-8
"""
Module of SqlCte class.
"""

__author__ = 'https://github.com/akvilary'

import uuid
from typing import Optional

from .sql_query import SqlQuery
from .sql_container import SqlContainer


class SqlCte(dict):
    """
    SqlCte class is invented for better experience with filling cte queries.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """
    def __init__(
        self,
        *args,
        sql_id: Optional[str | uuid.UUID] = '',
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.sql_id = sql_id

    def __call__(self) -> SqlContainer:
        result = SqlQuery(sql_id=self.sql_id) if self.sql_id else SqlQuery()
        counter = 0
        ctes_size = len(self)
        for cte_name, cte_query in self.items():
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
        query = sql_query if isinstance(sql_query, SqlQuery) else SqlQuery(**kwargs)
        self[cte_name] = query
        return query
