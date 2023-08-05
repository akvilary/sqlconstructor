import pytest
from sqlconstructor import SqlCol
from sqlconstructor import SqlContainer


@pytest.mark.SqlCol
def test_call():
    sql_col = SqlCol('a')
    container = sql_col(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '"a"'
    assert container.vars == {'y': 1, 'z': 2}
