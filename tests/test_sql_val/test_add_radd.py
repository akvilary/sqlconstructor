import pytest
from sqlconstructor import SqlVal


@pytest.mark.SqlVal
def test_add():
    assert (SqlVal('Best') + " or 'Medium'") == "'Best' or 'Medium'"


@pytest.mark.SqlVal
def test_radd():
    assert ('quality=' + SqlVal('Best')) == "quality='Best'"
