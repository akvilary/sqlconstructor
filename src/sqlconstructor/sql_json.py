# coding=utf-8
"""
Module of SqlJson class.
"""

__author__ = 'https://github.com/akvilary'

import json

from .sql_val.converters.to_json import convert_dict_to_sql_json


class SqlJson:
    """The class is invented to convert make conversion json-sql-json"""
    @staticmethod
    def dumps(json_obj: dict | list | str):
        """Convert from json to sql str"""
        return convert_dict_to_sql_json(json_obj)

    @staticmethod
    def loads(sql_obj: str):
        """Convert from normal or sql json to python dict"""
        converted = sql_obj[1:] if sql_obj.startswith('E') else sql_obj
        converted = converted[1:] if converted.startswith("'") else converted
        converted = converted[:-1] if converted.endswith("'") else converted
        return json.loads(converted)
