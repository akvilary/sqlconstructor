# coding=utf-8
"""
Module of SqlEnum class.
"""

__author__ = 'https://github.com/akvilary'

from collections import UserList
from typing import Any

from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.special_convertion_requier import SpecialConvertionRequier


class SqlEnum(StringConvertible, SpecialConvertionRequier, UserList):
    """
    SqlEnum class is invented for better experience to enumerate.
    """
    def __init__(
        self,
        *statements: Any,
    ):
        UserList.__init__(self, statements)

    def __str__(self) -> str:
        return str(self.multiline().wrap())

    def __as_sql__(self) -> str:
        return str(self.inline())

    def __as_json__(self) -> list:
        return list(str(x) for x in self)

    def __add__(self, other) -> str:
        return self.__as_sql__() + str(other)

    def __radd__(self, other) -> str:
        return str(other) + self.__as_sql__()

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(str(x) for x in self))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(str(x) for x in self))

    def copy(self):
        return SqlEnum(*self.data.copy())
