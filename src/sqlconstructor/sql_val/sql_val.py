# coding=utf-8
"""
Module of SqlVal class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any

from . import converters
from sqlconstructor.utils.classes.string_convertible import StringConvertible
from sqlconstructor.utils.classes.container_convertible import ContainerConvertible
from sqlconstructor.utils.classes.json_convertion_requier import JsonConvertionRequier


class SqlVal(StringConvertible, JsonConvertionRequier, ContainerConvertible):
    """
    SqlVal class is invented for better experience to convert any value to sql string.
    """
    def __init__(
        self,
        statement: Any,
    ):
        self.statement = statement

    def __str__(self) -> str:
        return converters.convert_any_to_sql(self.statement).replace(r'\\', '\\')

    def __as_json__(self) -> str:
        return converters.convert_any_to_sql(self.statement, is_json_context=True).replace(r'\\', '\\')
