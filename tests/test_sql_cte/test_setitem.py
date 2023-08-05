import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_set_query_as_cte():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    ctes['abc'] = q
    assert len(ctes) == 1
