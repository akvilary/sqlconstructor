import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_set_variables_by_calling_container():
    sql_text = 'quality = $quality AND brand_id = $brand_id'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    make_common_assertions(container)


@pytest.mark.SqlContainer
def test_set_variables_with_type_casting_by_calling_container():
    sql_text = 'quality = $quality::text AND brand_id = $brand_id::int'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    make_common_assertions(container, type_casting=True)


@pytest.mark.SqlContainer
def test_set_variables_by_vars_attribute():
    sql_text = 'quality = $quality AND brand_id = $brand_id'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container.vars['quality'] ='Best'
    container.vars['brand_id'] = 1
    make_common_assertions(container)


def make_common_assertions(container, type_casting = False):
    assert len(container.vars) == 2
    # check that in str representation placeholders are not replaced by vars
    assert 'Best' not in str(container)
    assert '1' not in str(container)
    # check that placeholders are replaced by vars only in 'dumps' method result
    if type_casting:
        assert container.dumps() == "quality = 'Best'::text AND brand_id = 1::int"
    else:
        assert container.dumps() == "quality = 'Best' AND brand_id = 1"
