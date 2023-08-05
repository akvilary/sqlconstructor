import pytest
from sqlconstructor import SqlQuery
from fixtures.expected_examples import select_section_of_simple_query_sql


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple():
    q = SqlQuery()
    q.add('abc xyz')
    container = q()
    assert str(container) == 'abc xyz'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple_to_filled_query(select_section_of_simple_query_sql):
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q.add('abc xyz')
    container = q()
    assert str(container) == (select_section_of_simple_query_sql + '\nabc xyz')


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple_by_magic_add():
    q = _q = SqlQuery()
    q += 'abc xyz'
    container = q()
    assert str(container) == 'abc xyz'
    assert q is _q


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_inherit_vars_of_containers_in_add_method():
    q = SqlQuery()
    subquery = SqlQuery()
    subquery['select']('$id', '$name')(id=1, name='phone')
    subquery_container = subquery()
    q += subquery_container
    query_container = q()
    assert query_container.vars == subquery_container.vars
    assert query_container.dumps() == "SELECT\n  1,\n  'phone'"
