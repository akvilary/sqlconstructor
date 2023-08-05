# coding=utf-8
"""Helpers which are used in multiple modules"""

__author__ = 'https://github.com/akvilary'

import re
import uuid
import json
from typing import Tuple

def indent_lines(text: str, ind: int) -> str:
    """Indent each line of the string"""
    text = ''.join((' ' * ind) + x + '\n' for x in text.splitlines()).rstrip()
    return text


def upper_keywords(text: str, keywords: Tuple[str]) -> str:
    """Upper certain keywords in string (case insensitive)"""
    for keyword in keywords:
        if keyword.lower() in text.lower():
            pattern = (
                r'(--.*?\Z)|(\/\*[\s\S]*?\*\/)|(".*?")|(\'.*?\')|'
                r'\b' + keyword + r'\b'
            )
            text = re.sub(
                pattern,
                upper_keyword_if_required,
                text,
                flags=re.I,
            )
    return text


def upper_keyword_if_required(match):
    """
    Upper keyword if keyword:
    1) Located not in inline sql comment
    2) Located not in multiline sql comment
    3) Located not between single quotes
    4) Located not between double quotes
    """
    groups = match.groups()
    if any(groups):
        return match.group()
    return match.group().upper()


def convert_to_sql_repr(value) -> str:
    """Convert any value to sql representation"""
    if isinstance(value, str):
        return convert_to_sql_str(value)
    if isinstance(value, (list, set, tuple)):
        return str('ARRAY[' + ', '.join(convert_to_sql_repr(x) for x in value) + ']')
    if isinstance(value, dict):
        return convert_dict_to_sql_repr(value)
    if isinstance(value, uuid.UUID):
        return convert_to_sql_str(value)
    return str(value)


def convert_to_sql_str(value) -> str:
    """Convert python string to sql string"""
    return f"'{value}'"


class SqlEncoder(json.JSONEncoder):
    """
    Custom json encoder.
    Add support for:
        - uuid
    """
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        return json.JSONEncoder.default(self, o)


def convert_dict_to_sql_repr(dictionary: dict) -> str:
    """Convert python dictionary to sql representation"""
    return json.dumps(dictionary, cls=SqlEncoder)


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
        + indent_lines(text, ind=2)
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
