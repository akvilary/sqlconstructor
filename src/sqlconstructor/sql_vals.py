# coding=utf-8
"""
Module of SqlVals class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Iterable

from .sql_container import SqlContainer
from .sql_enum import SqlEnum
from .sql_val import SqlVal


class SqlVals(SqlEnum):
    """
    SqlVals class is invented for better experience to convert python values to sql strings.
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
    return (str(SqlVal(x)) for x in iterable)
