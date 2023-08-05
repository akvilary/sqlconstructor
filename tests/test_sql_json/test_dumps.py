import pytest
from sqlconstructor import SqlJson, SqlContainer, SqlVal, SqlCol, SqlFilter


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


@pytest.mark.SqlJson
@pytest.mark.SqlVal
def test_dumps_dict_with_val():
    obj = {'a': SqlVal('b')}
    result = SqlJson.dumps(obj)
    assert result == """E'{"a": "\\\'b\\\'"}'"""


@pytest.mark.SqlJson
@pytest.mark.SqlCol
def test_dumps_dict_with_col():
    obj = {'a': SqlCol('b')}
    result = SqlJson.dumps(obj)
    assert result == """E'{"a": "\\\\"b\\\\""}'"""


@pytest.mark.SqlJson
@pytest.mark.SqlFilter
def test_dumps_dict_with_filter_as_str():
    obj = {'a': SqlFilter('b')}
    result = SqlJson.dumps(obj)
    assert result == """E'{"a": "b"}'"""


@pytest.mark.SqlJson
@pytest.mark.SqlFilter
def test_dumps_dict_with_filter_as_dict():
    obj = {'a': SqlFilter({'b': 'c'})}
    result = SqlJson.dumps(obj)
    assert result == """E'{"a": "b=\\\'c\\\'"}'"""
