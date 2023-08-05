# coding=utf-8
"""
Module of SqlCols class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_enum import SqlEnum
from .sql_col import SqlCol
from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.special_convertion_requier import SpecialConvertionRequier
from .utils.classes.container_convertible import ContainerConvertible


class SqlCols(SqlEnum, StringConvertible, SpecialConvertionRequier, ContainerConvertible):
    """
    SqlCols class is invented for better experience to enumerate as sql columns.
    """
    def __str__(self) -> str:
        """Convert SqlCols instance to str"""
        return str(self.multiline().wrap())

    def __as_sql__(self) -> str:
        return str(self.inline())

    def __as_json__(self) -> list:
        return list(str(SqlCol(x)) for x in self)

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        container = SqlContainer(', '.join(get_columns(self)))
        container.is_multiline_wrap_type = False
        return container

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_columns(self)))

    def copy(self):
        return SqlCols(*self.data.copy())


def get_columns(iterable: Iterable):
    """Get columns iterator"""
    return (str(SqlCol(x)) for x in iterable)
