import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_wrap():
    text = 'abc'
    wrapper_text = 'xyz'
    container = SqlContainer(text)
    _container = container.wrap(wrapper_text)
    assert container is _container
    assert str(container) == '(\n  abc\n) xyz'
