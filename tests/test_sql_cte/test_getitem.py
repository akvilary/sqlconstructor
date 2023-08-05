import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_get_query():
    _q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    ctes['abc'] = _q
    assert len(ctes) == 1
    q = ctes['abc']
    assert q is _q
    assert isinstance(q, SqlQuery)
