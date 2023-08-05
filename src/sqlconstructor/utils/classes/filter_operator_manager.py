# coding=utf-8
"""
Module of FilterOperatorManager class.
"""

__author__ = 'https://github.com/akvilary'

from sqlconstructor.constants import AND, OR
from sqlconstructor import sql_container as s_c
from .string_convertible import StringConvertible


class FilterOperatorManager(StringConvertible):
    """
    The class is invented to provide __and__, __rand__, __or__, __ror__ methods.
    It requires subclasses to have __str__ method.
    """

    def __and__(self, other):  # return SqlContainer
        return gather_filters(self, other, AND)

    def __rand__(self, other):  # return SqlContainer
        return gather_filters(other, self, AND)

    def __or__(self, other):  # return SqlContainer
        return gather_filters(self, other, OR)

    def __ror__(self, other):  # return SqlContainer
        return gather_filters(other, self, OR)


def gather_filters(
    one: StringConvertible,
    another: StringConvertible,
    operator: str,
):  # return SqlContainer
    """Gather two filters by operator"""
    filters = []
    united_vars = {}

    for _filter in (one, another):
        if isinstance(_filter, s_c.SqlContainer):
            united_vars.update(_filter.vars)

        filter_as_str = str(_filter)
        if filter_as_str:
            filters.append(filter_as_str)
    text = ('\n' + operator + '\n').join(filters)

    container = s_c.SqlContainer(text)
    container.vars = united_vars
    return container
