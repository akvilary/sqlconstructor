# coding=utf-8
"""
Module of SqlCols class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_enum import SqlEnum
from .sql_col import SqlCol
from .sql_container import SqlContainer


class SqlCols(SqlEnum):
    """
    SqlCols class is invented for better experience to enumerate as sql columns.
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
    return (str(SqlCol(x)) for x in iterable)
