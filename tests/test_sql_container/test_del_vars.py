import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_del_all_vars_of_container():
    sql_text = 'quality = $quality AND brand_id = $brand_id'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    assert len(container.vars) == 2

    container.vars.clear()
    assert len(container.vars) == 0
    assert container.dumps() == sql_text


@pytest.mark.SqlContainer
def test_del_certain_var_of_container():
    sql_text = 'quality = $quality AND brand_id = $brand_id'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    assert len(container.vars) == 2

    del container.vars['quality']
    assert len(container.vars) == 1
    assert 'quality = $quality AND brand_id = 1' == container.dumps()
