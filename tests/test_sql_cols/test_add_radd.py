import pytest
from sqlconstructor import SqlCols


@pytest.mark.SqlCols
def test_add():
    assert SqlCols('a', 'b') + 'c' == '"a", "b"c'


@pytest.mark.SqlCols
def test_radd():
    assert 'c' + SqlCols('a', 'b') == 'c"a", "b"'
