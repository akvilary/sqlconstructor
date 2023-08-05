# coding=utf-8
"""
Module of SqlContainer class.
"""

__author__ = 'https://github.com/akvilary'

from typing import Optional, Self, Any

import re

from .sql_val import SqlVal
from .utils.classes.filter_operator_manager import FilterOperatorManager
from .utils.classes.string_convertible import StringConvertible
from .utils.wrap_text import get_wrapped
from .utils.indent_text import indent_lines


class SqlContainer(FilterOperatorManager, StringConvertible):
    """SqlContainer is invented to store prepared SQL text and is an end result of
    any SQL constracting manipulations (it is a product of SqlSection and SqlQuery instances).

    Instance of SqlContainer class contains:
        1) self.text: str - body of SQL block as text;
        2) self.wrapper_text: str (if required by user) - this parameter treated as
            "wrap SQL body with parentheses and add wrapper_text after parentheses".
            If you call 'wrap' method then parentheses will automatically wrap main SQL text block,
            and wrapper_text will be added after wrapped parentheses (if you have provided it).
            If wrapper_text is empty string then you get text wrapped with only parentheses;
        3) self.vars: dict - variables for replacement
            which are useful if you have passed placeholders in SQL body
            (placeholder starts with $ character and is continued by an word with no space,
            $my_var for example) and want replace placeholders by variables.
            You could:
                - set variables by calling instance of SqlContainer with any keyword arguments
                (which all will be added to self.vars)
                - and get SQL text where placeholders are replaced by self.vars
                if you call self.dumps() method.
    """

    def __init__(
        self,
        text: str | StringConvertible,
    ):
        self.text: str = str(text)

        self.wrapper_text: Optional[str | StringConvertible] = None
        self.is_multiline_wrap_type: bool = True

        self.ind: int = 0  # relative indentation

        self.vars: dict = {}
        unite_container_vars(self, text)

    def __bool__(self):
        """True if self.text is True"""
        return bool(self.text)

    def __call__(self, **kwargs) -> Self:
        """Let you pass keyword arguments for later use in replacement job"""
        self.vars.update(kwargs)
        return self

    def __str__(self) -> str:
        """Convert SqlContainer instance to str"""
        return get_string_representation(
            self.text,
            self.wrapper_text,
            self.is_multiline_wrap_type,
            self.ind,
        )

    def dumps(self) -> str:
        """Get SqlContainer as str and do replace placeholders by self.vars
        if the latter were set (you could set vars by __call__ method).
        Notice: self.get method do not replace in self.text attribute.
        It process replacement and give string as a result.
        """
        text = self.text
        if text and self.vars:
            for keyword, value in self.vars.items():
                pattern = r'\$' + keyword + r'\b'
                converted_value = lambda _: str(SqlVal(value))
                text = re.sub(
                    pattern,
                    converted_value,
                    text,
                )
        return get_string_representation(
            text,
            self.wrapper_text,
            self.is_multiline_wrap_type,
            self.ind,
        )

    def wrap(self, wrapper_text: str | StringConvertible = '', do_multiline: bool = None) -> Self:
        """
        Set wrapper and text after it (optional).
        Params:
            - wrapper_text: is text after wrapped parentheses.
            - do_multiline:
                - if True then add parentheses in separate lines
                and indent text body inside (but it do not split self.text in multi lines).
                - if False then parentheses will be added without new lines and self.text will be
                not extra indented (but it do not convert self.text in one line).

        """
        self.wrapper_text = wrapper_text or ''
        if do_multiline is not None:
            self.is_multiline_wrap_type = do_multiline
        return self

    def unwrap(self) -> Self:
        """Delete wrapper and set default values"""
        self.wrapper_text = None
        self.is_multiline_wrap_type = True
        return self

    def indent(self, ind: int) -> Self:
        """Add extra relative indentation for string representation"""
        self.ind = ind
        return self


def get_string_representation(
    text: str,
    wrapper_text: Optional[str],
    is_wrap_multiline: bool = True,
    ind: int = 0,
) -> str:
    """Get text or wrap text by wrapper and return as string"""
    if wrapper_text is not None:
        return get_wrapped(
            text,
            wrapper_text or '',
            is_wrap_multiline,
            ind,
        )
    return indent_lines(str(text), ind) if ind else str(text)


def unite_container_vars(container: SqlContainer, obj: Any):
    """Unite container vars"""
    if isinstance(obj, SqlContainer):
        container.vars.update(obj.vars)
