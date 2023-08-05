# coding=utf-8
"""
Module of Values class.
"""

__author__ = 'https://github.com/akvilary'

from . import helpers
from .sql_enum import SqlEnum


class Vals(SqlEnum):
    """
    Values class is invented for better experience to enumerate values.
    It is possible to register cte and fill it after.
    Or you could add filled query as cte instantly.
    Now it is your choice!
    """

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        text = ',\n'.join(helpers.convert_to_sql_repr(x) for x in self)
        return helpers.get_text_wrapped(text, '')
