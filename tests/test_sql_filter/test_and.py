import pytest
from sqlconstructor import SqlFilter, AND


@pytest.mark.SqlFilter
def test_and_two_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    assert str(first_filter & second_filter) == '\n'.join(
        (
            'a=1',
            AND,
            'b=2',
        )
    )

@pytest.mark.SqlFilter
def test_and_three_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    third_filter = SqlFilter(c=3)
    assert str(first_filter & second_filter & third_filter) == '\n'.join(
        (
            'a=1',
            AND,
            'b=2',
            AND,
            'c=3',
        )
    )
