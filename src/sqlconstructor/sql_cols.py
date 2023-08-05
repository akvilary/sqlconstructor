# coding=utf-8
"""
Module of SqlCols class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_enum import SqlEnum
from .sql_col import SqlCol
from .sql_container import SqlContainer
from .abstracts.string_convertible import StringConvertible
from .abstracts.inline_enum import InlineEnum


class SqlCols(SqlEnum, StringConvertible, InlineEnum):
    """
    SqlCols class is invented for better experience to enumerate as sql columns.
    """

    def __str__(self) -> str:
        """Convert SqlCols instance to str"""
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
