import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_dumps():
    container = SqlContainer('id=$id name=$name')(id=1, name='phone')
    assert container.dumps() == "id=1 name='phone'"


@pytest.mark.SqlContainer
def test_dumps_repeated_placeholder():
    container = SqlContainer('a=$id AND b=$id')(id=1)
    assert container.dumps() == 'a=1 AND b=1'
