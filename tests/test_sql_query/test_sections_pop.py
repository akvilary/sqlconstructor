import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
def test_pop_from_empty_query():
    q = SqlQuery()
    assert len(q) == 0
    with pytest.raises(IndexError):
        q.sections.pop()


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_pop_from_filled_query():
    q = SqlQuery()
    header = 'SELECT'
    _section = q[header]
    assert len(q) == 1
    section = q.sections.pop()
    assert section is _section
    assert len(q) == 0
    container = q()
    assert str(container) == ''
