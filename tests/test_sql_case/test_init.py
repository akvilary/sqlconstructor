import pytest
from sqlconstructor import SqlCase


@pytest.mark.SqlCase
def test_init():
    sql_case = SqlCase(('b=1', 'one'), ('b=2', 'two'), 'nothing')
    assert isinstance(sql_case, SqlCase)
