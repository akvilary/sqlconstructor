# coding=utf-8
"""
Module of SqlPlaceholder class.
"""

__author__ = 'https://github.com/akvilary'


class SqlPlaceholder:
    """
    SqlPlaceholder class is invented for better experience to recieve placeholder.
    """
    def __init__(
        self,
        name: str,
    ):
        self.converted = '$' + name

    def __repr__(self) -> str:
        return self.converted

    def __str__(self) -> str:
        return repr(self)
