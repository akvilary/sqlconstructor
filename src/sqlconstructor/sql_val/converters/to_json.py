# coding=utf-8
"""
Module for converter from dict to json
"""

__author__ = 'https://github.com/akvilary'

import uuid
import json

from sqlconstructor.constants import DIALECT
from sqlconstructor.utils.classes.string_convertible import StringConvertible
from sqlconstructor.utils.classes.json_convertion_requier import JsonConvertionRequier


class SqlEncoder(json.JSONEncoder):
    """
    Custom json encoder.
    Add support for:
        - uuid
    """

    def default(self, o):
        if isinstance(o, JsonConvertionRequier):
            return o.__as_json__()
        if isinstance(
            o,
            (uuid.UUID, StringConvertible),
        ):
            return str(o)
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


def convert_dict_to_sql_json(dictionary: dict | list | str) -> str:
    """Convert python dictionary to sql representation"""
    return f"""{'E' if DIALECT == 'PostgreSQL' else ''}'{json.dumps(dictionary, cls=SqlEncoder)}'"""
