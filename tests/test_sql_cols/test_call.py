import pytest
from sqlconstructor import SqlCols
from sqlconstructor import SqlContainer


@pytest.mark.SqlCols
def test_call():
    sql_cols = SqlCols('a', 'b')
    container = sql_cols(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '\n'.join(
        (
            '(',
            '  "a",',
            '  "b"',
            ')',
        )
    )
    assert container.vars == {'y': 1, 'z': 2}
