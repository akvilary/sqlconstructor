import pytest
from sqlconstructor import SqlFilters


@pytest.mark.SqlFilters
def test_len():
    filters = SqlFilters({'a': 1, 'b': 2})
    assert len(filters) == 2


@pytest.mark.SqlFilters
def test_contains():
    filters = SqlFilters({'a': 1, 'b': 2})
    assert 'a' in filters


@pytest.mark.SqlFilters
def test_setitem():
    filters = SqlFilters()
    filters['a'] = 1
    assert len(filters) == 1


@pytest.mark.SqlFilters
def test_getitem():
    filters = SqlFilters({'a':1})
    assert filters['a'] == 1


@pytest.mark.SqlFilters
def test_del():
    filters = SqlFilters({'a':1})
    assert len(filters) == 1
    del filters['a']
    assert len(filters) == 0


@pytest.mark.SqlFilters
def test_popitem():
    filters = SqlFilters({'a':1})
    assert filters.popitem() == ('a', 1)


@pytest.mark.SqlFilters
def test_pop():
    filters = SqlFilters({'a':1})
    assert filters.pop('a') == 1


@pytest.mark.SqlFilters
def test_values():
    assert list(SqlFilters({'a': 1, 'b': 2}).values()) == [1, 2]


@pytest.mark.SqlFilters
def test_items():
    assert list(SqlFilters({'a': 1, 'b': 2}).items()) == [('a', 1), ('b', 2)]


@pytest.mark.SqlFilters
def test_clear():
    filters = SqlFilters({'a': 1, 'b': 2})
    assert len(filters) == 2
    filters.clear()
    assert len(filters) == 0
