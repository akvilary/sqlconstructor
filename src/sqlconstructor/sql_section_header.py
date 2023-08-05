# coding=utf-8
"""
Module of SqlSectionHeader class.
"""

__author__ = 'https://github.com/akvilary'


class SqlSectionHeader:
    """Class to make sql section header unique in dict"""
    def __init__(self, header: str):
        self.as_string = header

    def __str__(self):
        return self.as_string
