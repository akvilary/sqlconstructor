import pytest
from sqlconstructor import SqlWrap, SqlFilter, SqlPlaceholder, SqlContainer, AND, OR


@pytest.mark.SqlWrap
@pytest.mark.SqlContainer
def test_string_representation():
    assert str(SqlWrap('a')) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )


@pytest.mark.SqlWrap
@pytest.mark.SqlContainer
def test_string_representation_fake_wrapper_text():
    assert str(SqlWrap('a', None)) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )


@pytest.mark.SqlWrap
@pytest.mark.SqlFilter
@pytest.mark.SqlContainer
def test_wrap_filters():
    first_filter = SqlFilter(a=1)
    second_filter = SqlFilter(b=2)
    assert str(SqlWrap(first_filter & second_filter)) == '\n'.join(
        (
            '(',
            '  a=1',
            '  ' + AND,
            '  b=2',
            ')',
        )
    )


@pytest.mark.SqlWrap
@pytest.mark.SqlFilter
@pytest.mark.SqlPlaceholder
@pytest.mark.SqlContainer
def test_wrap_and_filters():
    filters = (
        'id <> $identifier'  # add placeholder in string
        & SqlFilter(  # AND operator
            brand_id=SqlPlaceholder(
                'brand_id'
            )  # add placeholder as value (you could insert SqlPlaceholder anywhere where value is expected)
        )  # will be converted to brand_id=$brand_id
        & SqlFilter(
            'quantity > 0'
        )  # string will not be converted by SqlVal and will be passed as is
        & SqlWrap(
            SqlFilter(quality='Best')  # value will be converted to sql string by SqlVal
            | SqlFilter(  # OR operator
                {'rating': 'high'}
            )  # each value of dict will be converted by SqlVal
        )
    )
    assert isinstance(filters, SqlContainer)
    assert str(filters) == '\n'.join(
        (
            'id <> $identifier',
            AND,
            'brand_id=$brand_id',
            AND,
            'quantity > 0',
            AND,
            '(',
            "  quality='Best'",
            '  ' + OR,
            "  rating='high'",
            ')',
        )
    )
