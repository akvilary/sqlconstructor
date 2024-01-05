import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_check_container_of_section_after_calling_section():
    q = SqlQuery()
    section = q['select']
    container = section(
        'id',
        'name',
    )
    assert section.container is not None
    assert section.container is container


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_inherit_vars_of_containers_in_section_call_method():
    q = SqlQuery()
    subquery = SqlQuery()
    subquery['']('$id', '$name')(id=1, name='phone')
    subquery_container = subquery()
    query_container = q[''](subquery_container)
    assert query_container.vars == subquery_container.vars
    assert query_container.dumps() == "1\n'phone'"


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_call_section_with_positive_header_ind_and_body_ind():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
        header_ind=2,
        body_ind=4,
    )
    container = q()
    assert str(container) == '\n'.join(
        (
            '  SELECT',
            '    id,',
            '    name',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_call_section_with_negative_header_ind_and_body_ind():
    q = SqlQuery()
    q['  select'](
        '    id',
        '    name',
        header_ind=-2,
        body_ind=-2,
    )
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_call_section_with_negative_header_ind_and_body_ind_beyond_bound():
    q = SqlQuery()
    q['  select'](
        '    id',
        '    name',
        header_ind=-4,
        body_ind=-4,
    )
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            'id,',
            'name',
        )
    )
