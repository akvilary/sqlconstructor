import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_add():
    assert SqlContainer('a') + 'b' == 'ab'


@pytest.mark.SqlContainer
def test_radd():
    assert 'b' + SqlContainer('a') == 'ba'
