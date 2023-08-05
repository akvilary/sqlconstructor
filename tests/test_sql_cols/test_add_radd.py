import pytest
from sqlconstructor import SqlCols


@pytest.mark.SqlCols
def test_add():
    assert SqlCols('a', 'b') + 'c' == '(\n  "a",\n  "b"\n)c'


@pytest.mark.SqlCols
def test_add_inline():
    assert SqlCols('a', 'b').inline() + 'c' == '"a", "b"c'


@pytest.mark.SqlCols
def test_radd():
    assert 'c' + SqlCols('a', 'b') == 'c(\n  "a",\n  "b"\n)'


@pytest.mark.SqlCols
def test_radd_inline():
    assert 'c' + SqlCols('a', 'b').inline() == 'c"a", "b"'
