import pytest
from sqlconstructor import SqlQuery, SqlSection, SqlContainer

from fixtures.expected_examples import simple_query_sql


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
def test_insert_and_get_sql_section():
    q = SqlQuery()
    assert isinstance(
        q['select'],
        SqlSection,
    )
    assert len(q.sections) == 1


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_get_container_from_calling_section():
    q = SqlQuery()
    assert isinstance(
        q['select'](
            'id',
            'name',
        ),
        SqlContainer,
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_building_query(simple_query_sql):
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    q['where'](
        "quality = 'Best'",
        'and brand_id = 1',
    )
    assert len(q.sections) == 3
    container = q()
    assert str(container) == simple_query_sql
