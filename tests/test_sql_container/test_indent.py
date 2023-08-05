import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_indent():
    container = SqlContainer('a').indent(2)
    assert str(container) == '  a'


@pytest.mark.SqlContainer
def test_indent_and_wrap():
    container = SqlContainer('a').wrap().indent(2)
    assert str(container) == '\n'.join(
        (
            '  (',
            '    a',
            '  )',
        )
    )
