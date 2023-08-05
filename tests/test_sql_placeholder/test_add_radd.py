import pytest
from sqlconstructor import SqlPlaceholder


@pytest.mark.SqlPlaceholder
def test_add():
    assert str(SqlPlaceholder('a') + 'b') == '$ab'

@pytest.mark.SqlPlaceholder
def test_radd():
    assert str('b' + SqlPlaceholder('a')) == 'b$a'
