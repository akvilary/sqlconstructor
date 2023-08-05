import pytest
import json
from sqlconstructor import SqlJson, SqlContainer


def test_loads_to_dict():
    assert SqlJson.loads("""'{"a": "b"}'""") == {'a': 'b'}


def test_loads_postgres_to_dict():
    assert SqlJson.loads("""E'{"a": "b"}'""") == {'a': 'b'}


def test_loads_to_list():
    assert SqlJson.loads("""'["a", "b"]'""") == ['a', 'b']


def test_loads_postgres_to_list():
    assert SqlJson.loads("""E'["a", "b"]'""") == ['a', 'b']


def test_loads_postgres_from_column_list():
    assert SqlJson.loads("""E'["\\"product\\"", "\\"quantity\\""]'""") == [
        '"product"',
        '"quantity"',
    ]
