import pytest
from sqlconstructor import SqlCte, SqlQuery


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_iter_ctes():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = q
    counter = 0
    for cte_name in ctes:
        assert isinstance(cte_name, str)
        assert cte_name == _cte_name
        counter += 1
    assert counter == 1


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_iter_ctes_keys():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = q
    counter = 0
    for cte_name in ctes.keys():
        assert isinstance(cte_name, str)
        assert cte_name == _cte_name
        counter += 1
    assert counter == 1


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_iter_ctes_values():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = q
    counter = 0
    for cte_query in ctes.values():
        assert isinstance(cte_query, SqlQuery)
        assert cte_query is q
        counter += 1
    assert counter == 1


@pytest.mark.SqlCte
@pytest.mark.SqlQuery
def test_iter_ctes_items():
    q = SqlQuery()
    ctes = SqlCte()
    assert len(ctes) == 0
    _cte_name = 'abc'
    ctes[_cte_name] = q
    counter = 0
    for cte_name, cte_query in ctes.items():
        assert isinstance(cte_name, str)
        assert cte_name == _cte_name

        assert isinstance(cte_query, SqlQuery)
        assert cte_query is q
        counter += 1
    assert counter == 1
