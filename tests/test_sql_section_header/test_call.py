import pytest
from sqlconstructor import SqlSectionHeader
from sqlconstructor import SqlContainer


@pytest.mark.SqlSectionHeader
def test_call():
    sql_section_header = SqlSectionHeader('a')
    container = sql_section_header(y=1, z=2)
    assert type(container) is SqlContainer
    assert str(container) == 'a'
    assert container.vars == {'y': 1, 'z': 2}
