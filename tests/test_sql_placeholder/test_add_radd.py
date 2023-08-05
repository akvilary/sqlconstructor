import pytest
from sqlconstructor import SqlPlaceholder


@pytest.mark.SqlPlaceholder
def test_add():
    assert SqlPlaceholder('a') + 'b' == '$ab'

@pytest.mark.SqlPlaceholder
def test_radd():
    assert 'b' + SqlPlaceholder('a') == 'b$a'
