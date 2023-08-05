import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_ctes_clear():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = q
    assert len(ctes) == 1
    ctes.clear()
    assert len(ctes) == 0
