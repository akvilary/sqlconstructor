# coding=utf-8
"""
Module of SqlFilter class.
"""

__author__ = 'https://github.com/akvilary'

from .utils.classes.string_convertible import StringConvertible
from .utils import indent_text


class SqlWrap(StringConvertible):
    def __init__(self, text: str | StringConvertible, wrapper_text: str | StringConvertible = ''):
        """Wrap text by parentheses and add wrapper_text after them.
        wrapper_text could be empty string (in that case you get text wrapped only by parentheses).
        Params:
            - text: str - text to be wrapped
            - wrapper_text: str - string to be added after parentheses enclosing "text" argument.
        """
        wrapper_text = str(wrapper_text)
        self.converted = (
            '('
            + '\n'
            + indent_text.indent_lines(str(text), ind=2)
            + '\n'
            + ')'
            + (
                wrapper_text
                if wrapper_text == ','
                else (' ' + wrapper_text)
                if wrapper_text
                else ''
            )
        )

    def __str__(self):
        return self.converted
