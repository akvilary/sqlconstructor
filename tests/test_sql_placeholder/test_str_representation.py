import pytest
from sqlconstructor import SqlPlaceholder


@pytest.mark.SqlPlaceholder
def test_string_representation():
    assert str(SqlPlaceholder('name')) == '$name'
