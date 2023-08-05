import pytest
from sqlconstructor import SqlWrap


@pytest.mark.SqlWrap
def test_add():
    assert str(SqlWrap('a') + 'b') == '(\n  a\n)b'

@pytest.mark.SqlWrap
def test_radd():
    assert str('b' + SqlWrap('a')) == 'b(\n  a\n)'
