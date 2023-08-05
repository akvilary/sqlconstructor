import pytest
from sqlconstructor import SqlWrap
from sqlconstructor import SqlContainer


@pytest.mark.SqlWrap
def test_call():
    sql_wrap = SqlWrap('a')
    container = sql_wrap(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )
    assert container.vars == {'y': 1, 'z': 2}
