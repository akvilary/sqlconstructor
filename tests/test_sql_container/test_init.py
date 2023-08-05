import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_init_with_text():
    text = 'a'
    container = SqlContainer(text)
    assert container.text == text
