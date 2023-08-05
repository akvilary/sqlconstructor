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
from .abstracts.special_json_convertible import SpecialJsonConvertible


class SqlCols(SqlEnum, StringConvertible, SpecialJsonConvertible):
    """
    SqlCols class is invented for better experience to enumerate as sql columns.
    """
    def __str__(self) -> str:
        """Convert SqlCols instance to str"""
        return str(self.multiline().wrap())

    def __json_str__(self) -> str:
        return str(self.inline())

    def __json_array__(self) -> list:
        return list('\"' + x + '\"' for x in self)

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(get_columns(self)))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_columns(self)))


def get_columns(iterable: Iterable):
    """Get columns iterator"""
    return (str(SqlCol(x)) for x in iterable)
