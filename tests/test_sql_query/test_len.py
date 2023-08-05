import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_len_of_empty_sql_query():
    q = SqlQuery()
    assert len(q) == 0


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_len_of_filled_sql_query():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    assert len(q) == 1
