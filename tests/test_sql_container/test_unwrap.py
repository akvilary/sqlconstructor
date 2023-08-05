import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_unwrap():
    text = 'abc'
    wrapper_text = 'xyz'
    container = SqlContainer(text)
    container.wrap(wrapper_text)
    assert str(container) == f'(\n  {text}\n) {wrapper_text}'
    container.unwrap()
    assert str(container) == text
