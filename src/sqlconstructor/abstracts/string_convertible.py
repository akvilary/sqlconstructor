# coding=utf-8
"""
Module of StringConvertible class.
"""

__author__ = 'https://github.com/akvilary'


class StringConvertible:
    """
    StringConvertible class is invented to group all supplementary classes 
    which provide '__str__' method.
    """
    def __str__(self):
        raise NotImplementedError()
