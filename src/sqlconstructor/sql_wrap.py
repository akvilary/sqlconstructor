# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from .sql_container import SqlContainer
from .utils.classes.filter_operator_manager import FilterOperatorManager
from .utils.classes.string_convertible import StringConvertible
from .utils.classes.container_convertible import ContainerConvertible


class SqlWrap(
    FilterOperatorManager,
    StringConvertible,
    ContainerConvertible,
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
        self.text = text
        self.wrapper_text = wrapper_text or ''

    def __str__(self):
        return str(SqlContainer(self.text).wrap(self.wrapper_text))

    def __call__(self, **kwargs):
        container = self.multiline()
        return ContainerConvertible.__call__(self, container, **kwargs)

    def inline(self) -> SqlContainer:
        """Get container of wrapped sql text in inline"""
        return SqlContainer(self.text).wrap(self.wrapper_text, multiline=False)

    def multiline(self) -> SqlContainer:
        """Get container of wrapped sql text in multiline"""
        return SqlContainer(self.text).wrap(self.wrapper_text)
