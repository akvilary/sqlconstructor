# coding=utf-8
"""
Module of StringConvertible class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC, abstractmethod
from .adder_class import Adder


class StringConvertible(ABC, Adder):
    """
    StringConvertible class is invented to group all supplementary classes 
    which provide '__str__' method.
    """
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()
