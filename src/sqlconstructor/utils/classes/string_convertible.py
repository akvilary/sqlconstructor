# coding=utf-8
"""
Module of StringConvertible class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC, abstractmethod
from .string_convertible_concatenator import StringConvertibleConcatenator


class StringConvertible(StringConvertibleConcatenator, ABC):
    """
    StringConvertible class is invented to group all supplementary classes 
    which provide '__str__' method.
    """
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()
