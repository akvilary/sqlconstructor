# coding=utf-8
"""
Module of SqlContainer class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Optional, Self

import re
import uuid

from . import helpers


class SqlContainer:
    """SqlContainer is invented to store prepared SQL text and is an end result of 
    any SQL constracting manipulations (it is a product of SqlSection and SqlQuery instances).

    Instance of SqlContainer class contains:
        1) self.text: str - body of SQL block as text; 
        2) self.wrapper_text: str (if required by user) - this parameter treated as 
            "wrap SQL body with parentheses and add wrapper_text after parentheses". 
            If you add wrapper_text (empty string is also possible) 
            then parentheses will automatically wrap main SQL text block, 
            and wrapper_text will be added after wrapped parentheses.
            If wrapper_text is empty string then you get text wrapped with only parentheses;
        3) self.vars: dict - variables for replacement
            which are useful if you have passed placeholders in SQL body
            (placeholder starts with ! character and is continued by an word with no space,
            !my_var for example) and want replace placeholders by variables.
            You could: 
                - set variables by calling instance of SqlContainer with any keyword arguments 
                (which all will be added to self.vars) 
                - and get SQL text where placeholders are replaced by self.vars 
                if you call self.get() method.
    """
    def __init__(self, text: str, wrapper_text: Optional[str] = None):
        self.text: str = text
        self.wrapper_text: Optional[str] = wrapper_text
        self.vars: dict = {}

    def __bool__(self):
        """True if self.text is True"""
        return bool(self.text)

    def __call__(self, **kwargs) -> Self:
        """Let you pass keyword arguments for later use in replacement job"""
        self.vars = kwargs
        return self

    def __repr__(self) -> str:
        """Convert SqlContainer instance to str"""
        return get_string_representation(self.text, self.wrapper_text)

    def __str__(self) -> str:
        """Return SqlContainer as str"""
        return repr(self)

    def get(self) -> str:
        """Get SqlContainer as str and do replace placeholders by self.vars 
        if the latter were set (you could set vars by __call__ method).
        Notice: self.get method do not replace in self.text attribute. 
        It process replacement and give string as a result.
        """
        text = self.text
        if text and self.vars:
            for keyword, value in self.vars.items():
                pattern = r'\!' + keyword + r'\b'
                text = re.sub(
                    pattern,
                    convert_to_sql_repr(value),
                    text,
                )
        return get_string_representation(text, self.wrapper_text)

    def wrap(self, text_after_wrapper: str = '') -> Self:
        """Set wrapper and text after it (optional)"""
        self.wrapper_text = text_after_wrapper or ''
        return self

    def unwrap(self) -> Self:
        """Delete wrapper"""
        self.wrapper_text = None
        return self


def get_string_representation(text, wrapper_text) -> str:
    """Get text or wrap text by wrapper and return as string"""
    if wrapper_text is not None:
        return get_text_wrapped(text, wrapper_text)
    return text


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
        + helpers.indent_lines(text, ind=2)
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


def convert_dict_to_sql_repr(dictionary: dict) -> str:
    """Convert python dictionary to sql representation"""
    converted = 'json_build_object('
    unzipped = []
    for key, value in dictionary.items():
        for item in (key, value):
            unzipped.append(convert_to_sql_repr(item))
    converted += ', '.join(unzipped)
    converted += ')'
    return converted
