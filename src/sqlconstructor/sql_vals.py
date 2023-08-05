# coding=utf-8
"""
Module of Values class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .helpers import converters
from .sql_container import SqlContainer
from .sql_enum import SqlEnum


class SqlVals(SqlEnum):
    """
    Values class is invented for better experience to enumerate values.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        return str(self.multiline().wrap())

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(get_values(self)))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_values(self)))


def get_values(iterable: Iterable):
    """Get values iterator"""
    return (converters.convert_any_to_sql(x) for x in iterable)
