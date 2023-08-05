import pytest
from sqlconstructor import SqlCol


@pytest.mark.SqlCol
def test_string_representation():
    assert str(SqlCol('product')) == '"product"'
