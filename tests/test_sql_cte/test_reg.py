import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_reg_new():
    ctes = SqlCte()
    assert len(ctes) == 0
    q = ctes.reg('abc')
    assert isinstance(q, SqlQuery)
    assert len(ctes) == 1


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_reg_existent():
    _q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    q = ctes.reg('abc', _q)
    assert q is _q
    assert isinstance(q, SqlQuery)
    assert len(ctes) == 1
