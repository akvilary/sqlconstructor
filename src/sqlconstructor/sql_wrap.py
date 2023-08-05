# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Self

from .sql_container import SqlContainer
from .utils.classes.string_convertible import StringConvertible


class SqlWrap(
    SqlContainer,
    StringConvertible,
):
    """The class is invented to do wrapping of sql text more easier"""

    def __init__(
        self,
        text: str | StringConvertible,
        wrapper_text: str | StringConvertible = '',
    ):
        """Wrap text by parentheses and add wrapper_text after them.
        wrapper_text could be empty string (in that case you get text wrapped only by parentheses).
        Params:
            - text: str - text to be wrapped
            - wrapper_text: str - string to be added after parentheses enclosing "text" argument.
        """
        SqlContainer.__init__(self, text)
        self.wrap(wrapper_text)

    def inline(self) -> Self:
        """Set inline option"""
        self.is_multiline_wrap_type = False
        return self

    def multiline(self) -> Self:
        """Set multiline option"""
        self.is_multiline_wrap_type = True
        return self
