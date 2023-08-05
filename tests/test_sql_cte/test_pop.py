import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_pop_from_filled_ctes():
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


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_pop_from_empty_ctes():
    ctes = SqlCte()
    assert len(ctes) == 0
    with pytest.raises(KeyError):
        ctes.pop('abc')
