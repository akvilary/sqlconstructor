# coding=utf-8
"""
Module for converter to sql representation
"""

__author__ = 'https://github.com/akvilary'

import uuid

from sqlconstructor.abstracts.string_convertible import StringConvertible
from sqlconstructor.abstracts.special_json_convertible import SpecialJsonConvertible
from . import to_sql_string
from . import to_array
from . import to_json


def convert_any_to_sql(value) -> str:
    """Convert any value to sql representation"""
    if isinstance(value, str):
        return to_sql_string.convert_python_str_to_sql_str(value)
    if isinstance(value, SpecialJsonConvertible):
        return value.__json_str__()
    if isinstance(value, StringConvertible):
        return str(value)
    if isinstance(value, (list, set, tuple)):
        return to_array.convert_to_sql_array(value)
    if isinstance(value, dict):
        return to_json.convert_dict_to_sql_json(value)
    if isinstance(value, uuid.UUID):
        return to_sql_string.convert_python_str_to_sql_str(value)
    if value is None:
        return 'null'
    return str(value)
