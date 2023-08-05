import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_convert_none_to_null():
    assert str(SqlVal(None)) == 'null'

@pytest.mark.SqlVal
def test_convert_none_to_null_in_dict_value():
    assert str(SqlVal({'a': None})) == '{"a": null}'
