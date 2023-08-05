import pytest
from sqlconstructor import SqlQuery

from fixtures.expected_examples import simple_query_sql
from fixtures.simple_query_dict import simple_query_dict


@pytest.mark.SqlQuery
def test_init_with_no_args():
    q = SqlQuery()
    assert isinstance(q, SqlQuery)


@pytest.mark.SqlQuery
def test_init_with_sql_id():
    sql_id = 'abc'
    q = SqlQuery(sql_id=sql_id)
    assert q.sql_id == sql_id


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_init_with_query(simple_query_dict, simple_query_sql):
    q = SqlQuery(simple_query_dict)
    assert len(q.sections) == 3
    container = q()
    assert str(container) == simple_query_sql
