import pytest
from sqlconstructor import SqlCol


@pytest.mark.SqlCol
def test_add():
    assert (SqlCol('a') + ' "b"') == '"a" "b"'


@pytest.mark.SqlVal
def test_radd():
    assert ('"a" ' + SqlCol('b')) == '"a" "b"'
