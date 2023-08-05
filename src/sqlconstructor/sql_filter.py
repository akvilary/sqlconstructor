# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Optional

from .sql_val import SqlVal
from .utils.classes.container_convertible import ContainerConvertible
from .utils.classes.filter_operator_manager import FilterOperatorManager
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.json_convertion_requier import JsonConvertionRequier


class SqlFilter(
    FilterOperatorManager,
    StringConvertible,
    JsonConvertionRequier,
    ContainerConvertible,
):
    """
    SqlFilter class is invented to build single sql keyword parameter faster.
    """

    def __init__(
        self,
        param: Optional[dict] | Optional[str | StringConvertible] = None,
        /,
        **kwargs,
    ):
        self.key, self.value = (
            param.popitem()  # take only last one
            if param and isinstance(param, dict)
            else (None, param)
            if param
            else kwargs.popitem()
        )

    def __str__(self):
        if self.key:
            return str(self.key) + '=' + str(SqlVal(self.value))
        return str(self.value)

    def __as_json__(self):
        if self.key:
            return str(self.key) + '=' + SqlVal(self.value).__as_json__()
        return str(self.value)
