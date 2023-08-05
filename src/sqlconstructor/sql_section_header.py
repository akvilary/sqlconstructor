# coding=utf-8
"""
Module of SqlSectionHeader class.
"""

__author__ = 'https://github.com/akvilary'

from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible


class SqlSectionHeader(StringConvertible, ContainerConvertible):
    """Class to make sql section header unique in dict"""
    def __init__(self, header: str = ''):
        self.as_string = header

    def __str__(self):
        return self.as_string
