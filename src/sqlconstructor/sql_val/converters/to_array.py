# coding=utf-8
"""
Module for converter to sql array
"""

__author__ = 'https://github.com/akvilary'

from . import any_to_sql


def convert_to_sql_array(iterable: list | set | tuple) -> str:
    """Convert to sql array"""
    return 'ARRAY[' + ', '.join(any_to_sql.convert_any_to_sql(x) for x in iterable) + ']'
