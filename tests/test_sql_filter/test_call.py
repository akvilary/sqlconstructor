import pytest
from sqlconstructor import SqlFilter
from sqlconstructor import SqlContainer


@pytest.mark.SqlFilter
def test_call():
    sql_filter = SqlFilter(a=3)
    container = sql_filter(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == 'a=3'
    assert container.vars == {'y': 1, 'z': 2}
