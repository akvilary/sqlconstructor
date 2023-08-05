# coding=utf-8
"""
Module of SqlConvertionRequier class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC, abstractmethod


class SqlConvertionRequier(ABC):
    """
    Class is invented to group all supplementary classes 
    which provide '__as_sql__' method.
    """
    @abstractmethod
    def __as_sql__(self) -> str:
        """Used to provide special convertion"""
        raise NotImplementedError()
