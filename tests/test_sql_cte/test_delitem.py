import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_del_cte():
    _q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    cte_name = 'abc'
    ctes[cte_name] = _q
    assert len(ctes) == 1
    del ctes[cte_name]
    assert len(ctes) == 0
