# coding=utf-8
"""
Module for converter from python string to sql string
"""

__author__ = 'https://github.com/akvilary'


def convert_python_str_to_sql_str(value, is_json_context: bool = False) -> str:
    """Convert python string to sql string"""
    prefix = postfix = "\\'" if is_json_context else "'"
    converted = f"""{prefix}{value}{postfix}"""
    return converted
