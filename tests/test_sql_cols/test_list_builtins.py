import pytest
from sqlconstructor import SqlCols


@pytest.mark.SqlCols
def test_len():
    assert len(SqlCols('a', 'b')) == 2


@pytest.mark.SqlCols
def test_contains():
    sql_cols = SqlCols('a', 'b')
    assert 'a' in sql_cols


@pytest.mark.SqlCols
def test_setitem():
    sql_cols = SqlCols('a', 'b')
    sql_cols[0] = 'c'
    assert list(sql_cols) == ['c', 'b']


@pytest.mark.SqlCols
def test_getitem():
    sql_cols = SqlCols('a', 'b')
    assert sql_cols[0] == 'a'
    assert sql_cols[1] == 'b'


@pytest.mark.SqlCols
def test_del():
    sql_cols = SqlCols('a', 'b')
    assert len(sql_cols) == 2
    del sql_cols[0]
    assert len(sql_cols) == 1


@pytest.mark.SqlCols
def test_append():
    sql_cols = SqlCols()
    assert len(sql_cols) == 0
    sql_cols.append('a')
    assert len(sql_cols) == 1
    assert list(sql_cols) == ['a']


@pytest.mark.SqlCols
def test_extend():
    sql_cols = SqlCols()
    assert len(sql_cols) == 0
    sql_cols.extend(['a', 'b'])
    assert len(sql_cols) == 2
    assert list(sql_cols) == ['a', 'b']


@pytest.mark.SqlCols
def test_pop():
    sql_cols = SqlCols('a')
    assert len(sql_cols) == 1
    assert sql_cols.pop() == 'a'
    assert len(sql_cols) == 0


@pytest.mark.SqlCols
def test_clear():
    sql_cols = SqlCols('a', 'b')
    assert len(sql_cols) == 2
    sql_cols.clear()
    assert len(sql_cols) == 0


@pytest.mark.SqlCols
def test_index():
    sql_cols = SqlCols('a', 'b')
    assert sql_cols.index('b') == 1


@pytest.mark.SqlCols
def test_sort():
    sql_cols = SqlCols('b', 'a')
    sql_cols.sort()
    assert list(sql_cols) == ['a', 'b']


@pytest.mark.SqlCols
def test_reverse():
    sql_cols = SqlCols('a', 'b')
    sql_cols.reverse()
    assert list(sql_cols) == ['b', 'a']

@pytest.mark.SqlCols
def test_insert():
    sql_cols = SqlCols('a', 'b')
    sql_cols.insert(0, 'c')
    assert list(sql_cols) == ['c', 'a', 'b']


@pytest.mark.SqlCols
def test_remove():
    sql_cols = SqlCols('a', 'b')
    sql_cols.remove('a')
    assert list(sql_cols) == ['b']


@pytest.mark.SqlCols
def test_count():
    sql_cols = SqlCols('a', 'a')
    assert sql_cols.count('a') == 2


@pytest.mark.SqlCols
def test_copy():
    sql_cols = SqlCols('a', 'b')
    assert list(sql_cols.copy()) == ['a', 'b']
