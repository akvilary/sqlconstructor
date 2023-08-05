import pytest
from sqlconstructor import SqlQuery

from fixtures.expected_examples import simple_query_sql
from fixtures.simple_query_dict import simple_query_dict_with_placeholders


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_building_query_with_variables(simple_query_sql):
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    q['where'](
        'quality = $quality',
        'AND brand_id = $brand_id',
    )(quality='Best', brand_id=1)
    container = q()
    make_common_assertions(container, simple_query_sql)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_set_variables_by_calling_container_after_building_query(
    simple_query_dict_with_placeholders,
    simple_query_sql,
):
    q = SqlQuery(simple_query_dict_with_placeholders)
    container = q()
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    make_common_assertions(container, simple_query_sql)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_set_variables_by_vars_attribute_after_building_query(
    simple_query_dict_with_placeholders,
    simple_query_sql,
):
    q = SqlQuery(simple_query_dict_with_placeholders)
    container = q()
    assert len(container.vars) == 0
    container.vars['quality'] = 'Best'
    container.vars['brand_id'] = 1
    make_common_assertions(container, simple_query_sql)


def make_common_assertions(container, simple_query_sql):
    assert len(container.vars) == 2
    # check that in str representation placeholders are not replaced by vars
    assert 'Best' not in str(container)
    assert '1' not in str(container)
    # check that placeholders are replaced by vars only in 'dumps' method result
    assert container.dumps() == simple_query_sql
