import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_reset_all_vars_of_container():
    sql_text = 'quality = $quality AND brand_id = $brand_id'
    container = SqlContainer(sql_text)
    assert len(container.vars) == 0
    container(quality='Best', brand_id=1)
    assert len(container.vars) == 2

    new_vars = {'quality': 'Medium'}
    container.vars = new_vars
    assert len(container.vars) == 1
    assert 'Medium' in container.dumps()
    assert '$brand_id' in container.dumps()
