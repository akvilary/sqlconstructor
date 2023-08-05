# coding=utf-8
"""
Module of StringConvertibleConcatenator class.
"""

__author__ = 'https://github.com/akvilary'

from sqlconstructor import sql_container as s_c


class StringConvertibleConcatenator:
    """
    The class is invented to provide add and radd method for StringConvertible.
    """
    def __add__(self, other):
        container = s_c.SqlContainer(str(self) + str(other))
        for arg in (self, other):
            s_c.unite_container_vars(container, arg)
        return container

    def __radd__(self, other):
        container = s_c.SqlContainer(str(other) + str(self))
        for arg in (self, other):
            s_c.unite_container_vars(container, arg)
        return container
