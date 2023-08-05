import pytest
from sqlconstructor import SqlVals


@pytest.mark.SqlVals
def test_len():
    assert len(SqlVals('a', 'b')) == 2


@pytest.mark.SqlVals
def test_contains():
    sql_vals = SqlVals('a', 'b')
    assert 'a' in sql_vals


@pytest.mark.SqlVals
def test_setitem():
    sql_vals = SqlVals('a', 'b')
    sql_vals[0] = 'c'
    assert list(sql_vals) == ['c', 'b']


@pytest.mark.SqlVals
def test_getitem():
    sql_vals = SqlVals('a', 'b')
    assert sql_vals[0] == 'a'
    assert sql_vals[1] == 'b'


@pytest.mark.SqlVals
def test_del():
    sql_vals = SqlVals('a', 'b')
    assert len(sql_vals) == 2
    del sql_vals[0]
    assert len(sql_vals) == 1


@pytest.mark.SqlVals
def test_append():
    sql_vals = SqlVals()
    assert len(sql_vals) == 0
    sql_vals.append('a')
    assert len(sql_vals) == 1
    assert list(sql_vals) == ['a']


@pytest.mark.SqlVals
def test_extend():
    sql_vals = SqlVals()
    assert len(sql_vals) == 0
    sql_vals.extend(['a', 'b'])
    assert len(sql_vals) == 2
    assert list(sql_vals) == ['a', 'b']


@pytest.mark.SqlVals
def test_pop():
    sql_vals = SqlVals('a')
    assert len(sql_vals) == 1
    assert sql_vals.pop() == 'a'
    assert len(sql_vals) == 0


@pytest.mark.SqlVals
def test_clear():
    sql_vals = SqlVals('a', 'b')
    assert len(sql_vals) == 2
    sql_vals.clear()
    assert len(sql_vals) == 0


@pytest.mark.SqlVals
def test_index():
    sql_vals = SqlVals('a', 'b')
    assert sql_vals.index('b') == 1


@pytest.mark.SqlVals
def test_sort():
    sql_vals = SqlVals('b', 'a')
    sql_vals.sort()
    assert list(sql_vals) == ['a', 'b']


@pytest.mark.SqlVals
def test_reverse():
    sql_vals = SqlVals('a', 'b')
    sql_vals.reverse()
    assert list(sql_vals) == ['b', 'a']

@pytest.mark.SqlVals
def test_insert():
    sql_vals = SqlVals('a', 'b')
    sql_vals.insert(0, 'c')
    assert list(sql_vals) == ['c', 'a', 'b']


@pytest.mark.SqlVals
def test_remove():
    sql_vals = SqlVals('a', 'b')
    sql_vals.remove('a')
    assert list(sql_vals) == ['b']


@pytest.mark.SqlVals
def test_count():
    sql_vals = SqlVals('a', 'a')
    assert sql_vals.count('a') == 2


@pytest.mark.SqlVals
def test_copy():
    sql_vals = SqlVals('a', 'b')
    assert list(sql_vals.copy()) == ['a', 'b']
