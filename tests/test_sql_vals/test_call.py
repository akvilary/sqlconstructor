import pytest
from sqlconstructor import SqlVals
from sqlconstructor import SqlContainer


@pytest.mark.SqlVals
def test_call():
    sql_vals = SqlVals('a', 'b')
    container = sql_vals(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '\n'.join(
        (
            '(',
            "  'a',",
            "  'b'",
            ')',
        )
    )
    assert container.vars == {'y': 1, 'z': 2}
