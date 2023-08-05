import pytest
from sqlconstructor import SqlFilters
from sqlconstructor.constants import AND_MODE


@pytest.mark.SqlFilters
def test_add():
    assert SqlFilters({'a': 1, 'b': 2}) + 'c' == '\n'.join(
        (
            'a=1',
            AND_MODE,
            'b=2c',
        )
    )


@pytest.mark.SqlFilters
def test_radd():
    assert 'c' + SqlFilters({'a': 1, 'b': 2}) == '\n'.join(
        (
            'ca=1',
            AND_MODE,
            'b=2',
        )
    )
