import pytest
from sqlconstructor import SqlQuery, SqlSection


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
def test_iter_of_filled_sql_query():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    counter = 0
    for section in q:
        assert isinstance(section, SqlSection)
        counter += 1
    assert counter == 1
