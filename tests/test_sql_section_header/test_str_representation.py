import pytest
from sqlconstructor import SqlSectionHeader


@pytest.mark.SqlSectionHeader
def test_string_representation_if_constructed_without_args():
    assert str(SqlSectionHeader()) == ''


@pytest.mark.SqlSectionHeader
def test_string_representation():
    string = 'hello'
    assert str(SqlSectionHeader(string)) == string
