import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_add():
    assert str(SqlContainer('a') + 'b') == 'ab'


@pytest.mark.SqlContainer
def test_radd():
    assert str('b' + SqlContainer('a')) == 'ba'
