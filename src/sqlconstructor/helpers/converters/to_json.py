# coding=utf-8
"""
Module for converter from dict to json
"""

__author__ = 'https://github.com/akvilary'

import uuid
import json

class SqlEncoder(json.JSONEncoder):
    """
    Custom json encoder.
    Add support for:
        - uuid
    """
    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, set):
            return tuple(o)
        return json.JSONEncoder.default(self, o)


def convert_dict_to_sql_json(dictionary: dict) -> str:
    """Convert python dictionary to sql representation"""
    return json.dumps(dictionary, cls=SqlEncoder)
