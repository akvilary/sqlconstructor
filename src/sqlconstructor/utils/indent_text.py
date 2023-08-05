# coding=utf-8
"""
Module for indentation helpers
"""

__author__ = 'https://github.com/akvilary'


def indent_lines(text: str, ind: int) -> str:
    """
    Indent each line of the string.
    Indentation could be positive or negative.
    """
    text = ''.join(
        ((' ' * ind) if ind >= 0 else '')
        + (
            x
            if ind >= 0
            else (
                x[
                    abs(
                        ind
                        if number_of_leading_spaces(x) >= abs(ind)
                        else number_of_leading_spaces(x)
                    ) :
                ]
            )
        )
        + '\n'
        for x in text.splitlines()
    ).rstrip()
    return text


def number_of_leading_spaces(line: str) -> int:
    """Return number of leading spaces"""
    return len(line) - len(line.lstrip())
