import pytest
from sqlconstructor import SqlWrap


@pytest.mark.SqlWrap
def test_inline():
    assert (
        str(
            SqlWrap(
                'a',
            ).inline()
        )
        == '(a)'
    )


@pytest.mark.SqlWrap
def test_inline_and_unwrap():
    container = SqlWrap('a').inline()
    assert str(container) == '(a)'
    assert str(container.unwrap()) == 'a'


@pytest.mark.SqlWrap
def test_inline_with_wrapper_text():
    container = SqlWrap(
        'a',
        'as b',
    ).inline()
    assert str(container) == '(a) as b'
