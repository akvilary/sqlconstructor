import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_add():
    assert str(SqlVal('a') + 'b')== "'a'b"


@pytest.mark.SqlVal
def test_radd():
    assert str('b' + SqlVal('a')) == "b'a'"
