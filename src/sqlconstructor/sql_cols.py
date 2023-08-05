# coding=utf-8
"""
Module of Cols class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_enum import SqlEnum
from .sql_container import SqlContainer


class SqlCols(SqlEnum):
    """
    Cols class is invented for better experience to enumerate columns.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        return str(self.multiline().wrap())

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(get_columns(self)))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_columns(self)))


def get_columns(iterable: Iterable):
    """Get columns iterator"""
    return ('"' + str(x) + '"' for x in iterable)
