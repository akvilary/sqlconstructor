# coding=utf-8
"""
Module of SpecialJsonConvertible class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC,abstractmethod


class SpecialJsonConvertible(ABC):
    """
    Class is invented to group all supplementary classes 
    which provide '__json_str__' method.
    """
    @abstractmethod
    def __json_str__(self) -> str:
        """Used to provide special convetrion"""
        raise NotImplementedError()

    @abstractmethod
    def __json_array__(self) -> list:
        """Used to provide special convetrion"""
        raise NotImplementedError()
