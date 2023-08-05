# coding=utf-8
"""
Module of SqlEnum class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any

from .sql_container import SqlContainer
from .abstracts.string_convertible import StringConvertible
from .abstracts.special_json_convertible import SpecialJsonConvertible


class SqlEnum(list, StringConvertible, SpecialJsonConvertible):
    """
    SqlEnum class is invented for better experience to enumerate.
    """
    def __init__(
        self,
        *statements: Any,
    ):
        super().__init__(statements)

    def __str__(self) -> str:
        return str(self.multiline().wrap())

    def __json_str__(self) -> str:
        return str(self.inline())

    def __json_array__(self) -> list:
        return list(str(x) for x in self)

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(str(x) for x in self))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(str(x) for x in self))
