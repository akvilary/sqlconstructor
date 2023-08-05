import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_bool_true_expected():
    text = 'abc'
    container = SqlContainer(text)
    assert bool(container) is True


@pytest.mark.SqlContainer
def test_bool_false_expected():
    text = ''
    container = SqlContainer(text)
    assert bool(container) is False
