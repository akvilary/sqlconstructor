import pytest
import uuid
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_convert_none_to_null():
    assert str(SqlVal(None)) == 'null'


@pytest.mark.SqlVal
def test_convert_none_to_null_in_dict_value():
    assert str(SqlVal({'a': None})) == '{"a": null}'


@pytest.mark.SqlVal
def test_convert_uuid():
    _uuid = uuid.uuid4()
    assert str(SqlVal(_uuid)) == f"'{_uuid}'"


@pytest.mark.SqlVal
def test_convert_uuid_in_dict_value():
    _uuid = uuid.uuid4()
    assert str(SqlVal({'a': _uuid})) == '{"a": ' + f'"{_uuid}"' + '}'
