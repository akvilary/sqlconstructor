# coding=utf-8
"""
Module for wrapping helpers
"""

__author__ = 'https://github.com/akvilary'

from . import indent_text


def get_text_wrapped(text: str, wrapper_text: str) -> str:
    """Wrap text by parentheses and add wrapper_text after them.
    wrapper_text could be empty string (in that case you get text wrapped only by parentheses).
    Params:
        - text: str - text to be wrapped
        - wrapper_text: str - string to be added after parentheses enclosing "text" argument.
    """
    return (
        '('
        + '\n'
        + indent_text.indent_lines(text, ind=2)
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
