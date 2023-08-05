import pytest
from sqlconstructor import SqlWrap, SqlFilter
from sqlconstructor.constants import AND_MODE


@pytest.mark.SqlWrap
def test_string_representation():
    assert str(SqlWrap('a')) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )

@pytest.mark.SqlWrap
@pytest.mark.SqlFilter
def test_wrap_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    assert str(SqlWrap(first_filter & second_filter)) == '\n'.join(
        (
            '(',
            '  a=1',
            '  ' + AND_MODE,
            '  b=2',
            ')',
        )
    )
