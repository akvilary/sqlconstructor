import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_convert_none_to_null():
    assert str(SqlVal(None)) == 'NULL'
