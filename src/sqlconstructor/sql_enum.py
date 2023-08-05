# coding=utf-8
"""
Module of SqlEnum class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any

from . import helpers


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
        return '(\n' + helpers.indent_lines(',\n'.join(x for x in self), ind=2) + '\n)'

    def __str__(self) -> str:
        """Return SqlContainer as str"""
        return repr(self)
