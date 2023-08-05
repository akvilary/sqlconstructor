import pytest

from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_array_variable():
    array = ['a', 'b']
    container = SqlContainer("$array")(array=array)
    assert container.dumps() == "ARRAY['a', 'b']"
