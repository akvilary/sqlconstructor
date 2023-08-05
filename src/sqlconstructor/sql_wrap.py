# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from .sql_container import SqlContainer
from .utils.classes.filter_operator_manager import FilterOperatorManager
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible
from .utils.wrap_text import get_wrapped


class SqlWrap(
    FilterOperatorManager,
    StringConvertible,
    ContainerConvertible,
):
    """The class is invented to do wrapping of sql text more easier"""
    def __init__(self, text: str | StringConvertible, wrapper_text: str | StringConvertible = ''):
        """Wrap text by parentheses and add wrapper_text after them.
        wrapper_text could be empty string (in that case you get text wrapped only by parentheses).
        Params:
            - text: str - text to be wrapped
            - wrapper_text: str - string to be added after parentheses enclosing "text" argument.
        """
        self.text = text
        self.wrapper_text = wrapper_text

    def __str__(self):
        return get_wrapped(self.text, self.wrapper_text)

    def inline(self) -> SqlContainer:
        """Get container of wrapped sql text in inline"""
        return SqlContainer(get_wrapped(self.text, self.wrapper_text, do_multiline=False))

    def multiline(self) -> SqlContainer:
        """Get container of wrapped sql text in multiline"""
        return SqlContainer(str(self))
