# coding=utf-8
"""
Module of SqlEnum class.
"""

__author__ = 'https://github.com/akvilary'

from collections import UserList
from typing import Any

from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible
from .utils.classes.json_convertion_requier import JsonConvertionRequier
from .utils.classes.sql_convertion_requier import SqlConvertionRequier


class SqlEnum(
    StringConvertible, JsonConvertionRequier, SqlConvertionRequier, ContainerConvertible, UserList
):
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

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        container = SqlContainer(', '.join(str(x) for x in self))
        container.is_multiline_wrap_type = False
        return container

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(str(x) for x in self))

    def copy(self):
        return SqlEnum(*self.data.copy())
