# coding=utf-8
"""
Module of Containerable class.
"""

__author__ = 'https://github.com/akvilary'

from sqlconstructor import sql_container as s_c


class ContainerConvertible:
    """
    Containerable class is invented to provide __call__ method 
    to convert subclass instance to SqlContainer.
    """
    def __call__(self, container = None, /, **kwargs):
        container = container if container is not None else s_c.SqlContainer(str(self))
        # add vars to container
        if kwargs:
            container(**kwargs)
        return container
