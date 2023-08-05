# coding=utf-8
"""
Module for helpers to upper sql keywords
"""

__author__ = 'https://github.com/akvilary'

from sqlconstructor.constants import DEFAULT_IND
from .classes.string_convertible import StringConvertible
from .indent_text import indent_lines


def get_wrapped(
    text: str | StringConvertible,
    wrapper_text: str | StringConvertible = '',
    is_wrap_multiline: bool = True,
    extra_indentation: int = 0,
) -> str:
    """Wrap and return as string"""
    text = str(text)
    wrapper_text = str(wrapper_text)

    return (
        ' ' * extra_indentation
        + '('
        + ('\n' if is_wrap_multiline else '')
        + indent_lines(
            str(text),
            ind=(DEFAULT_IND + extra_indentation) if is_wrap_multiline else 0 + (extra_indentation),
        )
        + ('\n' if is_wrap_multiline else '')
        + ' ' * extra_indentation
        + ')'
        + (
            wrapper_text
            if wrapper_text.startswith(',')
            else (' ' + wrapper_text)
            if wrapper_text
            else ''
        )
    )
