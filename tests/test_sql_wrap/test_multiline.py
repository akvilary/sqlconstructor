import pytest
from sqlconstructor import SqlWrap


@pytest.mark.SqlWrap
def test_multiline():
    container = SqlWrap('a').multiline()
    assert str(container) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )


@pytest.mark.SqlWrap
def test_multiline_and_unwrap():
    container = SqlWrap('a').multiline()
    assert str(container) == '\n'.join(
        (
            '(',
            '  a',
            ')',
        )
    )
    assert str(container.unwrap()) == 'a'


@pytest.mark.SqlWrap
def test_multiline_with_wrapper_text():
    container = SqlWrap(
        'a',
        'as b',
    ).multiline()
    assert str(container) == '\n'.join(
        (
            '(',
            '  a',
            ') as b',
        )
    )
