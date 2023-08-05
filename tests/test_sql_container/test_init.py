import pytest
from sqlconstructor import SqlContainer

TEXT = 'some'
WRAPPER_TEXT = 'another'


@pytest.mark.SqlContainer
@pytest.mark.parametrize("args, kwargs", [
    ([TEXT], {}),
    ([], {'text': TEXT}),
])
def test_init_with_text(args, kwargs):
    container = SqlContainer(*args, **kwargs)
    assert container.text == TEXT


@pytest.mark.SqlContainer
@pytest.mark.parametrize("args, kwargs", [
    ([TEXT, WRAPPER_TEXT], {}),
    ([TEXT], {'wrapper_text': WRAPPER_TEXT}),
])
def test_init_with_text_and_wrapper(args, kwargs):
    container = SqlContainer(*args, **kwargs)
    assert container.wrapper_text == WRAPPER_TEXT
