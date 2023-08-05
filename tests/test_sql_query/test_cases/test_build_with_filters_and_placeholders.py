import pytest
from sqlconstructor import SqlQuery, SqlSection, SqlContainer, SqlFilter, SqlPlaceholder
from sqlconstructor.constants import AND_MODE


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.SqlFilter
@pytest.mark.SqlPlaceholder
def test_build_query_with_filters_and_placeholders():
    product_quality = 'Best'

    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    q['where'](
        SqlFilter(quality=product_quality)
        &
        'id <> $id'
        &
        SqlFilter(
            brand_id=SqlPlaceholder('brand_id')  # it will be converted to brand_id=$brand_id
        )  # set placeholder to insert value later (after building query)
        &
        SqlFilter('quantity > 0')
    )
    container: SqlContainer = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name',
            'FROM',
            '  product',
            'WHERE',
            "  quality='Best'",
            '  ' + AND_MODE,
            '  id <> $id',
            '  ' + AND_MODE,
            '  brand_id=$brand_id',
            '  ' + AND_MODE,
            '  quantity > 0',
        )
    )
