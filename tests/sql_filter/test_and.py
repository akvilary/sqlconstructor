import pytest
from sqlconstructor import SqlFilter
from sqlconstructor.constants import AND_MODE


@pytest.mark.SqlFilter
def test_and_two_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    assert (first_filter & second_filter) == '\n'.join(
        (
            'a=1',
            AND_MODE,
            'b=2',
        )
    )

@pytest.mark.SqlFilter
def test_and_three_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    third_filter = SqlFilter(c=3)
    assert (first_filter & second_filter & third_filter) == '\n'.join(
        (
            'a=1',
            AND_MODE,
            'b=2',
            AND_MODE,
            'c=3',
        )
    )
