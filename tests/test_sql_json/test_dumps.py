import pytest
from sqlconstructor import SqlJson, SqlContainer


@pytest.mark.SqlJson
def test_dumps_dict():
    assert SqlJson.dumps({'a': 'b'}) == """E'{"a": "b"}'"""


@pytest.mark.SqlJson
def test_dumps_list():
    assert SqlJson.dumps(['a', 'b']) == """E'["a", "b"]'"""


@pytest.mark.SqlJson
@pytest.mark.SqlContainer
def test_dumps_dict_with_container():
    assert SqlJson.dumps({'a': SqlContainer('b')}) == """E'{"a": "b"}'"""
