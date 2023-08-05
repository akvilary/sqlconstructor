import pytest
from sqlconstructor import SqlFilter


@pytest.mark.SqlFilter
def test_add():
    assert str(SqlFilter(a=1) + 'b') == 'a=1b'


@pytest.mark.SqlFilter
def test_radd():
    assert str('b' + SqlFilter(a=1)) == 'ba=1'
