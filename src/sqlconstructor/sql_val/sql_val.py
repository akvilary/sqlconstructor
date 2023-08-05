# coding=utf-8
"""
Module of SqlVal class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any

from . import converters
from sqlconstructor.utils.classes.string_convertible import StringConvertible


class SqlVal(StringConvertible):
    """
    SqlVal class is invented for better experience to convert any value to sql string.
    """
    def __init__(
        self,
        statement: Any,
    ):
        self.converted = converters.convert_any_to_sql(statement)

    def __str__(self) -> str:
        return self.converted

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)
