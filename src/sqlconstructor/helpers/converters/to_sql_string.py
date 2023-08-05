# coding=utf-8
"""
Module for converter from python string to sql string
"""

__author__ = 'https://github.com/akvilary'


def convert_python_str_to_sql_str(value) -> str:
    """Convert python string to sql string"""
    return f"'{value}'"
