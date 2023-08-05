import pytest
from sqlconstructor import SqlVal
from sqlconstructor import SqlContainer


@pytest.mark.SqlVal
def test_call():
    sql_val = SqlVal('a')
    container = sql_val(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == "'a'"
    assert container.vars == {'y': 1, 'z': 2}
