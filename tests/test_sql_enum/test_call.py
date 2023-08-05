import pytest
from sqlconstructor import SqlEnum
from sqlconstructor import SqlContainer


@pytest.mark.SqlEnum
def test_call():
    sql_enum = SqlEnum('a', 'b')
    container = sql_enum(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '\n'.join(
        (
            '(',
            '  a,',
            '  b',
            ')',
        )
    )
    assert container.vars == {'y': 1, 'z': 2}
