# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Optional

from .constants import AND_MODE, OR_MODE
from .sql_val import SqlVal
from .utils.classes.string_convertible import StringConvertible


class SqlFilter(StringConvertible):
    """
    SqlFilter class is invented to build single sql keyword parameter faster.
    """

    def __init__(self, __param: Optional[dict] | Optional[str] = None, /, **kwargs):
        key, value = (
            __param.popitem() # take only last one
            if __param and isinstance(__param, dict)
            else (None, __param)
            if __param
            else kwargs.popitem()
        )
        if key:
            self.converted = str(key) + '=' + str(SqlVal(value))
        else:
            self.converted = str(value)

    def __str__(self):
        return self.converted

    def __and__(self, other):
        return gather_filters(self, other, AND_MODE)

    def __rand__(self, other):
        return gather_filters(other, self, AND_MODE)

    def __or__(self, other):
        return gather_filters(self, other, OR_MODE)

    def __ror__(self, other):
        return gather_filters(other, self, OR_MODE)


def gather_filters(one: SqlFilter, another: SqlFilter | str, operator: str) -> str:
    """Gather two filters by operator"""
    filters = []
    for _filter in (one, another):
        if _filter:
            filters.append(str(_filter))
    return ('\n' + operator + '\n').join(filters)
