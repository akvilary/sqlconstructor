import pytest
from sqlconstructor import SqlSection


@pytest.mark.SqlSection
def test_bool_false_expected():
    section = SqlSection('select')
    assert bool(section) is False


@pytest.mark.SqlSection
def test_bool_true_expected():
    section = SqlSection('select')
    section(
        'id',
        'name',
    )
    assert bool(section) is True
