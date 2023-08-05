import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_string_representation():
    assert str(SqlVal('hello')) == "'hello'"
