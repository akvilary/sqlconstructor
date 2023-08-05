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
def test_inline_with_wrapper_text():
    assert (
        str(
            SqlWrap(
                'a',
                'as b',
            ).inline()
        )
        == '(a) as b'
    )
