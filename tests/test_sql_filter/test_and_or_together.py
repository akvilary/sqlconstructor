import pytest
from sqlconstructor import SqlFilter, AND, OR


@pytest.fixture
def get_three_filters():
    return SqlFilter({'a': 1}), SqlFilter({'b': 2}), SqlFilter({'c': 3})


@pytest.mark.SqlFilter
def test_three_filters_or_and(get_three_filters):
    first_filter, second_filter, third_filter = get_three_filters
    assert str(first_filter | second_filter & third_filter) == '\n'.join(
        (
            'a=1',
            OR,
            'b=2',
            AND,
            'c=3',
        )
    )


@pytest.mark.SqlFilter
def test_three_filters_and_or(get_three_filters):
    first_filter, second_filter, third_filter = get_three_filters
    assert str(first_filter & second_filter | third_filter) == '\n'.join(
        (
            'a=1',
            AND,
            'b=2',
            OR,
            'c=3',
        )
    )
