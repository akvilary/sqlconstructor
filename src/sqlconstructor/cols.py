# coding=utf-8
"""
Module of Cols class.
"""

__author__ = 'https://github.com/akvilary'


from . import helpers
from .sql_enum import SqlEnum


class Cols(SqlEnum):
    """
    Cols class is invented for better experience to enumerate columns.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        return '(\n' + helpers.indent_lines(',\n'.join('"' + x + '"' for x in self), ind=2) + '\n)'
