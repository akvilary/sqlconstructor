import pytest

from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_array_variable():
    my_list = ['a', 'b']
    container = SqlContainer('$my_list')(my_list=my_list)
    assert container.dumps() == "ARRAY['a', 'b']"
