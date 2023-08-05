import pytest
from sqlconstructor import SqlPlaceholder
from sqlconstructor import SqlContainer


@pytest.mark.SqlPlaceholder
def test_call():
    sql_placeholder = SqlPlaceholder('a')
    container = sql_placeholder(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '$a'
    assert container.vars == {'y': 1, 'z': 2}
