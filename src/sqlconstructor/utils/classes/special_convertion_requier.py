# coding=utf-8
"""
Module of SpecialJsonConvertible class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC, abstractmethod


class SpecialConvertionRequier(ABC):
    """
    Class is invented to group all supplementary classes 
    which provide '__json_str__' method.
    """
    @abstractmethod
    def __as_sql__(self) -> str:
        """Used to provide special convetrion"""
        raise NotImplementedError()

    @abstractmethod
    def __as_json__(self) -> list:
        """Used to provide special convetrion"""
        raise NotImplementedError()
