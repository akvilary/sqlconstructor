import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_add():
    assert SqlVal('a') + 'b'== "'a'b"


@pytest.mark.SqlVal
def test_radd():
    assert ('b' + SqlVal('a')) == "b'a'"
