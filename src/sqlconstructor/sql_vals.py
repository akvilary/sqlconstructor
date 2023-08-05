# coding=utf-8
"""
Module of SqlVals class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_container import SqlContainer
from .sql_enum import SqlEnum
from .sql_val import SqlVal
from .utils.classes.container_convertible import ContainerConvertible
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.json_convertion_requier import JsonConvertionRequier
from .utils.classes.sql_convertion_requier import SqlConvertionRequier


class SqlVals(
    SqlEnum, StringConvertible, JsonConvertionRequier, SqlConvertionRequier, ContainerConvertible
):
    """
    SqlVals class is invented for better experience to convert python values to sql strings.
    """

    def __str__(self) -> str:
        """Convert SqlContainer instance to str"""
        return str(self.multiline().wrap())

    def __as_json__(self) -> list:
        return list(SqlVal(x).__as_json__() for x in self)

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        container = SqlContainer(', '.join(get_values(self)))
        container.is_multiline_wrap_type = False
        return container

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_values(self)))

    def copy(self):
        return SqlVals(*self.data.copy())


def get_values(iterable: Iterable):
    """Get values iterator"""
    return (str(SqlVal(x)) for x in iterable)
