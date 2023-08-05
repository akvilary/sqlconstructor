import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
def test_bool_true_expected():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    assert bool(q) is True


@pytest.mark.SqlQuery
def test_bool_false_expected():
    q = SqlQuery()
    assert bool(q) is False


@pytest.mark.SqlQuery
def test_bool_false_expected_after_clear():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q.sections.clear()
    assert bool(q) is False
