import pytest
from sqlconstructor import SqlFilter


@pytest.mark.SqlFilter
def test_string_representation():
    assert str(SqlFilter({'say': 'hello'})) == "say='hello'"
