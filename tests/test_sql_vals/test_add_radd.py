import pytest
from sqlconstructor import SqlVals


@pytest.mark.SqlVals
def test_add():
    assert SqlVals('a', 'b') + 'c' == "'a', 'b'c"


@pytest.mark.SqlVals
def test_radd():
    assert 'c' + SqlVals('a', 'b') == "c'a', 'b'"
