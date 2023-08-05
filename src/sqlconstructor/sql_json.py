# coding=utf-8
"""
Module of SqlJson class.
"""

__author__ = 'https://github.com/akvilary'

import json

from .sql_val.converters import to_json


class SqlJson:
    """The class is invented to convert make conversion json-sql-json"""
    @staticmethod
    def dumps(json_obj: dict | list | str):
        """Convert from json to sql str"""
        return to_json.convert_dict_to_sql_json(json_obj).replace(r'\\', '\\')

    @staticmethod
    def loads(sql_obj: str):
        """Convert from normal or sql json to python dict"""
        converted = sql_obj.removeprefix('E')
        converted = converted.removeprefix("'")
        converted = converted.removesuffix("'")
        return json.loads(converted)
