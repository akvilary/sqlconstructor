import pytest
from sqlconstructor import SqlQuery, SqlContainer


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_get_sql_container_if_call_empty_sql_query():
    q = SqlQuery()
    assert isinstance(q(), SqlContainer)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_get_sql_container_if_call_filled_sql_query():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    assert isinstance(q(), SqlContainer)
