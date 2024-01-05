import pytest
from sqlconstructor import nullif, SqlVal


@pytest.mark.sql_builtin_functions
def test_nullif_are_equal():
    result = nullif(3,3)
    assert result is None


@pytest.mark.sql_builtin_functions
def test_nullif_are_not_equal():
    result = nullif(3,4)
    assert result == 3


@pytest.mark.sql_builtin_functions
@pytest.mark.SqlVal
def test_nullif_are_equal_to_sql_val():
    assert str(SqlVal(nullif(3,3))) == 'null'
