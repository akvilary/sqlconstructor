# coding=utf-8
"""
Module of SqlCase class.
"""

__author__ = 'https://github.com/akvilary'

from collections import UserList

from .constants import DEFAULT_IND
from .sql_query import SqlQuery
from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible


class SqlCase(UserList, StringConvertible):
    """
    SqlCase class is invented to provide CASE-WHEN-THEN-ELSE interface.
    """

    def __init__(self, *statements):
        UserList.__init__(self, statements)

    def __call__(self) -> SqlContainer:
        branches = SqlQuery()
        for statement in self.data:
            if isinstance(statement, (tuple, list)):
                if len(statement) == 2:
                    branches['when'](statement[0])
                    branches['then'](statement[1])
            else:
                # it is not allowed to add else if branches query is empty
                if not branches:
                    raise ValueError(
                        'It is not allowed to add ELSE statement before WHEN-THEN statements'
                    )
                branches['else'](statement)
                break

        query = SqlQuery()
        if branches:
            query.add('case')
            query.add(branches(), ind=DEFAULT_IND)
            query.add('end')
        return query()

    def __str__(self):
        return str(self())
