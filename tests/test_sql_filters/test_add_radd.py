import pytest
from sqlconstructor import SqlFilters, AND


@pytest.mark.SqlFilters
def test_add():
    assert str(SqlFilters({'a': 1, 'b': 2}) + 'c') == '\n'.join(
        (
            'a=1',
            AND,
            'b=2c',
        )
    )


@pytest.mark.SqlFilters
def test_radd():
    assert str('c' + SqlFilters({'a': 1, 'b': 2})) == '\n'.join(
        (
            'ca=1',
            AND,
            'b=2',
        )
    )
