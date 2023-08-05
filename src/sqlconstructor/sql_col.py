# coding=utf-8
"""
Module of SqlCol class.
"""

__author__ = 'https://github.com/akvilary'

from .utils.classes.string_convertible import StringConvertible


class SqlCol(StringConvertible):
    """
    SqlCol class is invented for better experience to convert string to column.
    """
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return '"' + str(self.name) + '"'
