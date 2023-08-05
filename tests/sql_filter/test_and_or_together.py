import pytest
from sqlconstructor import SqlFilter
from sqlconstructor.constants import AND_MODE, OR_MODE


@pytest.fixture
def get_three_filters():
    return SqlFilter({'a': 1}), SqlFilter({'b': 2}), SqlFilter({'c': 3})


@pytest.mark.SqlFilter
def test_three_filters_or_and(get_three_filters):
    first_filter, second_filter, third_filter = get_three_filters
    assert (first_filter | second_filter & third_filter) == '\n'.join(
        (
            'a=1',
            OR_MODE,
            'b=2',
            AND_MODE,
            'c=3',
        )
    )


@pytest.mark.SqlFilter
def test_three_filters_and_or(get_three_filters):
    first_filter, second_filter, third_filter = get_three_filters
    assert (first_filter & second_filter | third_filter) == '\n'.join(
        (
            'a=1',
            AND_MODE,
            'b=2',
            OR_MODE,
            'c=3',
        )
    )
