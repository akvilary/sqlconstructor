import pytest
from sqlconstructor import SqlEnum


@pytest.mark.SqlEnum
def test_add():
    assert SqlEnum('a', 'b') + 'c' == 'a, bc'


@pytest.mark.SqlEnum
def test_radd():
    assert 'c' + SqlEnum('a', 'b') == 'ca, b'
