import pytest
from sqlconstructor import SqlCte, SqlContainer


@pytest.mark.SqlCte
@pytest.mark.SqlContainer
def test_call_empty_ctes():
    ctes = SqlCte()
    assert isinstance(ctes(), SqlContainer)


@pytest.mark.SqlCte
@pytest.mark.SqlContainer
@pytest.mark.SqlQuery
def test_call_filled_ctes():
    ctes = SqlCte()
    cte_name = 'aswithsome'
    q = ctes.reg(cte_name)
    q['select'](
        'id',
        'name',
    )
    container = ctes()
    assert isinstance(container, SqlContainer)
    assert str(ctes()) == f'WITH {cte_name} AS\n  (\n    SELECT\n      id,\n      name\n  )' 
