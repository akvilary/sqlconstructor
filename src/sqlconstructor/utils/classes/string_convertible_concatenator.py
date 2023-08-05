# coding=utf-8
"""
Module of StringConvertibleConcatenator class.
"""

__author__ = 'https://github.com/akvilary'


class StringConvertibleConcatenator:
    """
    The class is invented to provide add and radd method for StringConvertible.
    """
    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)
