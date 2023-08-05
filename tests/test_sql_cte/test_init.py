import pytest
from sqlconstructor import SqlCte


@pytest.mark.SqlCte
def test_init_with_no_args():
    ctes = SqlCte()
    assert isinstance(ctes, SqlCte)


@pytest.mark.SqlCte
def test_init_with_sql_id():
    sql_id = 'abc'
    ctes = SqlCte(sql_id=sql_id)
    assert ctes.sql_id == sql_id
    assert str(ctes()) == "-- sql_id='abc'"
