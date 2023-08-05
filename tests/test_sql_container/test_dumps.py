import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_dumps():
    container = SqlContainer('id=$id name=$name')(id=1, name='phone')
    assert container.dumps() == "id=1 name='phone'"
