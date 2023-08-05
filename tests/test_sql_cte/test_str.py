import pytest
from sqlconstructor import SqlCte


@pytest.mark.SqlCte
@pytest.mark.SqlContainer
def test_str_empty_cte():
    ctes = SqlCte()
    assert str(ctes) == ''


@pytest.mark.SqlCte
@pytest.mark.SqlContainer
@pytest.mark.SqlQuery
def test_str_filled_ctes():
    ctes = SqlCte()
    q = ctes.reg('a')
    q['select'](
        'id',
        'name',
    )
    assert str(ctes) == 'WITH a AS\n  (\n    SELECT\n      id,\n      name\n  )'
