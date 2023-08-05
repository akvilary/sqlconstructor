import pytest
from sqlconstructor import SqlContainer


@pytest.mark.SqlContainer
def test_positive_indent():
    container = SqlContainer('a').indent(2)
    assert str(container) == '  a'


@pytest.mark.SqlContainer
def test_negative_indent():
    container = SqlContainer('  a').indent(-2)
    assert str(container) == 'a'


@pytest.mark.SqlContainer
def test_negative_indent_if_indent_greater_than_number_of_leading_spaces():
    container = SqlContainer('  a').indent(-1000)
    assert str(container) == 'a'


@pytest.mark.SqlContainer
def test_positive_indent_and_wrap():
    container = SqlContainer('a').wrap().indent(2)
    assert str(container) == '\n'.join(
        (
            '  (',
            '    a',
            '  )',
        )
    )
