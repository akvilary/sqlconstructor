import pytest
from sqlconstructor import SqlCol


@pytest.mark.SqlCol
def test_add():
    assert (SqlCol('product') + ' "warehouse"') == '"product" "warehouse"'


@pytest.mark.SqlVal
def test_radd():
    assert ('"product" ' + SqlCol('warehouse')) == '"product" "warehouse"'
