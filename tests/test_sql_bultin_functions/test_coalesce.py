import pytest
from sqlconstructor import coalesce, SqlVal


@pytest.mark.sql_builtin_functions
def test_coalesce_not_none():
    result = coalesce(None, 3, 4, None)
    assert result == 3


@pytest.mark.sql_builtin_functions
def test_coalesce_all_none():
    result = coalesce(None, None, None)
    assert result is None

@pytest.mark.sql_builtin_functions
@pytest.mark.SqlVal
def test_coalesce_all_none_to_sql_val():
    assert str(SqlVal(coalesce(None, None))) == 'null'
