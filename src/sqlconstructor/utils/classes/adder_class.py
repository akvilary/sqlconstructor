# coding=utf-8
"""
Module of Adder class.
"""

__author__ = 'https://github.com/akvilary'


class Adder:
    """
    Adder is invented to provide add and radd method for StringConvertible.
    """
    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)
