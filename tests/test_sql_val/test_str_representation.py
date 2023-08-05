import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_string_representation():
    assert str(SqlVal('hello')) == "'hello'"


@pytest.mark.SqlVal
def test_string_representation_in_format_string():
    string = '\n'.join(
        (
            f"quality = {SqlVal('Best')}",
            f'and brand_id = {SqlVal(1)}',
        )
    )
    assert string == '\n'.join(
        (
            "quality = 'Best'",
            'and brand_id = 1',
        )
    )
