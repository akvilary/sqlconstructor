# coding=utf-8
"""
Module for indentation helpers
"""

__author__ = 'https://github.com/akvilary'


def indent_lines(text: str, ind: int) -> str:
    """Indent each line of the string"""
    text = ''.join((' ' * ind) + x + '\n' for x in text.splitlines()).rstrip()
    return text
