# coding=utf-8
"""
Module of JsonConvertionRequier class.
"""

__author__ = 'https://github.com/akvilary'

from abc import ABC, abstractmethod


class JsonConvertionRequier(ABC):
    """
    Class is invented to group all supplementary classes 
    which provide '__as_json__' method.
    """

    @abstractmethod
    def __as_json__(self) -> list:
        """Used to provide special convetrion"""
        raise NotImplementedError()
