import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_ctes_pop():
    _q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = _q
    assert len(ctes) == 1
    q = ctes.pop(_cte_name)
    assert len(ctes) == 0
    assert q is _q
    b = ctes.pop('xyz', None)
    assert b is None
