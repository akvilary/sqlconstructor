import pytest
from sqlconstructor import SqlFilter


@pytest.mark.SqlFilter
def test_add():
    assert SqlFilter(a=1) + 'b' == 'a=1b'


@pytest.mark.SqlFilter
def test_radd():
    assert 'b' + SqlFilter(a=1) == 'ba=1'
