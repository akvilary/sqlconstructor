# coding=utf-8
"""
Module of SqlPlaceholder class.
"""

__author__ = 'https://github.com/akvilary'

from .utils.classes.string_convertible import StringConvertible


class SqlPlaceholder(StringConvertible):
    """
    SqlPlaceholder class is invented for better experience to recieve placeholder.
    """
    def __init__(
        self,
        name: str,
    ):
        self.converted = '$' + name

    def __str__(self) -> str:
        return self.converted
