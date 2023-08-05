# coding=utf-8
"""
Module of Containerable class.
"""

__author__ = 'https://github.com/akvilary'

from sqlconstructor import sql_container as sc


class ContainerConvertible:
    """
    Containerable class is invented to provide __call__ method 
    to convert subclass instance to SqlContainer.
    """
    def __call__(self, **kwargs):
        container = sc.SqlContainer(str(self))
        if kwargs:
            container(**kwargs)
        return container
