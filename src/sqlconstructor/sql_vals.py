# coding=utf-8
"""
Module of SqlVals class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_container import SqlContainer
from .sql_enum import SqlEnum
from .sql_val import SqlVal
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.special_convertion_requier import SpecialConvertionRequier


class SqlVals(SqlEnum, StringConvertible, SpecialConvertionRequier):
    """
    SqlVals class is invented for better experience to convert python values to sql strings.
    """

    def __str__(self) -> str:
        """Convert SqlContainer instance to str"""
        return str(self.multiline().wrap())

    def __json_str__(self) -> str:
        return str(self.inline())

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(get_values(self)))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(get_values(self)))

    def copy(self, /):
        return SqlVals(list(self.list))


def get_values(iterable: Iterable):
    """Get values iterator"""
    return (str(SqlVal(x)) for x in iterable)
