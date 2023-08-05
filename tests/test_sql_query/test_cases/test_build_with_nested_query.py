import pytest
from sqlconstructor import SqlQuery, SqlContainer, SqlWrap


def get_nested_subquery(avg_column, partition_column):
    q = SqlQuery()
    q['AVG']('$avg_column')(avg_column=avg_column)
    q['OVER'](SqlWrap('PARTITION BY $partition_column'))(
        partition_column=partition_column
    )
    return q


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.SqlWrap
def test_build_nested_with_sql_query_instance_as_sbuquery():
    avg_column = SqlContainer('price')
    partition_column = SqlContainer('name')
    q = SqlQuery()
    q['select'](
        'id',
        'name',
        get_nested_subquery(avg_column=avg_column, partition_column=partition_column),
    )
    container = q()
    assert container.dumps() == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name,',
            '  AVG',
            '    price',
            '  OVER',
            '    (',
            '      PARTITION BY name',
            '    )',
        )
    )
    assert container.vars == {'avg_column': avg_column, 'partition_column': partition_column}
