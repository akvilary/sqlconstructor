# coding=utf-8
"""
Module of SqlFilters class.
"""

__author__ = 'https://github.com/akvilary'

from collections import UserDict
from typing import Optional

from .constants import AND, OR
from .sql_filter import SqlFilter
from .utils.classes.filter_operator_manager import FilterOperatorManager
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible


class SqlFilters(FilterOperatorManager, StringConvertible, ContainerConvertible, UserDict):
    """
    SqlFilters class is invented to build sql filters faster.
    """

    def __init__(self, filters: Optional[dict] = None, mode: str = AND, /, **kwargs):
        united_filters = {}
        if filters:
            united_filters.update(filters)
        if kwargs:
            united_filters.update(kwargs)
        UserDict.__init__(self, united_filters)

        self.mode = mode

    def __str__(self):
        converted = ''
        if self:
            method = (
                '__rand__'
                if self.mode.upper() == AND
                else '__ror__'
                if self.mode.upper() == OR
                else None
            )
            if method:
                for key, value in self.items():
                    current_filter = SqlFilter({key: value})
                    converted = getattr(current_filter, method)(converted)
        return str(converted)
