import pytest
from sqlconstructor import SqlFilters, SqlContainer, AND


@pytest.mark.SqlFilters
def test_call():
    sql_filter = SqlFilters(a=3, b=4)
    container = sql_filter(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == '\n'.join(
        (
            'a=3',
            AND,
            'b=4',
        )
    )
    assert container.vars == {'y': 1, 'z': 2}
