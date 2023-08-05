# coding=utf-8
"""
Module of ProxyList class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Any


class ProxyList:
    """
    ProxyList is invented to not inherit from builin (it is required for custom json encoder).
    """
    def __init__(
        self,
        *statements: Any,
    ):
        self.list = list(statements)

    def __add__(self, value, /):
        return self.list + value

    def __radd__(self, value, /):
        return value + self.list

    def __contains__(self, key, /):
        return key in self.list

    def __delitem__(self, key, /):
        del self.list[key]

    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, key):
        return self.list[key]

    def append(self, other: list):
        """Append method"""
        self.list.append(other)

    def extend(self, iterable, /):
        """Append method"""
        self.list.extend(iterable)

    def __eq__(self, value, /):
        return self.list == value

    def __ge__(self, value, /):
        return self.list >= value

    def __gt__(self, value, /):
        return self.list > value

    def __iadd__(self, value, /):
        return self.list + value

    def __imul__(self, value, /):
        return self.list * value

    def __le__(self, value, /):
        return self.list <= value

    def __len__(self, /):
        return len(self.list)

    def __lt__(self, value, /):
        return self.list < value

    def __mul__(self, value, /):
        return self.list * value

    def __ne__(self, value, /):
        return self.list != value

    def __reversed__(self, /):
        return self.list.__reversed__()

    def __rmul__(self, value, /):
        return value * self.list

    def __setitem__(self, key, value, /):
        self.list[key] = value

    def clear(self, /):
        self.list.clear()

    def copy(self, /):
        return NotImplemented

    def count(self, *args, **kwargs):
        return self.list.count(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.list.index(*args, **kwargs)

    def insert(self, *args, **kwargs):
        self.list.insert(*args, **kwargs)

    def pop(self, *args, **kwargs):
        """Append method"""
        return self.list.pop(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self.list.remove(*args, **kwargs)

    def reverse(self):
        return self.list.reverse()

    def sort(self, *args, **kwargs):
        return self.list.sort(*args, **kwargs)
