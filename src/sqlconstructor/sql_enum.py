# coding=utf-8
"""
Module of SqlEnum class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any

from .sql_container import SqlContainer


class SqlEnum(list):
    """
    SqlEnum class is invented for better experience to enumerate.
    """
    def __init__(
        self,
        *statements: Any,
    ):
        super().__init__(statements)

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        return str(self.multiline().wrap())

    def __str__(self) -> str:
        """Return SqlContainer as str"""
        return repr(self)

    def inline(self) -> SqlContainer:
        """Get inline representation"""
        return SqlContainer(', '.join(str(x) for x in self))

    def multiline(self) -> SqlContainer:
        """Get multiline representation"""
        return SqlContainer(',\n'.join(str(x) for x in self))
