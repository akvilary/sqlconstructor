# coding=utf-8
"""
Module for builtins sql funtions for python
"""

__author__ = 'https://github.com/akvilary'

from typing import Any


def coalesce(*args) -> Any:
    """
    Get first not None arg.
    If all args will be None then return None.
    """
    for arg in args:
        if arg is not None:
            return arg
    return None


def nullif(first: Any, second: Any, /) -> Any:
    """
    If two arguments will be equal then return None.
    Return first argument otherwise.
    """
    if first == second:
        return None
    return first
