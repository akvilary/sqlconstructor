import pytest
from sqlconstructor import SqlVals


@pytest.mark.SqlVals
def test_add():
    assert SqlVals('a', 'b') + 'c' == "(\n  'a',\n  'b'\n)c"


@pytest.mark.SqlVals
def test_add_inline():
    assert SqlVals('a', 'b').inline() + 'c' == "'a', 'b'c"


@pytest.mark.SqlVals
def test_radd():
    assert 'c' + SqlVals('a', 'b') == "c(\n  'a',\n  'b'\n)"


@pytest.mark.SqlVals
def test_radd_inline():
    assert 'c' + SqlVals('a', 'b').inline() == "c'a', 'b'"
