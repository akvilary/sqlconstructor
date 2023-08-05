# coding=utf-8
"""
Module of SqlPlaceholder class.
"""

__author__ = 'https://github.com/akvilary'

from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible


class SqlPlaceholder(StringConvertible, ContainerConvertible):
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
