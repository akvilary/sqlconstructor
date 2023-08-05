import pytest
from sqlconstructor import SqlEnum


@pytest.mark.SqlEnum
def test_len():
    assert len(SqlEnum('a', 'b')) == 2


@pytest.mark.SqlEnum
def test_contains():
    sql_enum = SqlEnum('a', 'b')
    assert 'a' in sql_enum


@pytest.mark.SqlEnum
def test_setitem():
    sql_enum = SqlEnum('a', 'b')
    sql_enum[0] = 'c'
    assert list(sql_enum) == ['c', 'b']


@pytest.mark.SqlEnum
def test_getitem():
    sql_enum = SqlEnum('a', 'b')
    assert sql_enum[0] == 'a'
    assert sql_enum[1] == 'b'


@pytest.mark.SqlEnum
def test_del():
    sql_enum = SqlEnum('a', 'b')
    assert len(sql_enum) == 2
    del sql_enum[0]
    assert len(sql_enum) == 1


@pytest.mark.SqlEnum
def test_append():
    sql_enum = SqlEnum()
    assert len(sql_enum) == 0
    sql_enum.append('a')
    assert len(sql_enum) == 1
    assert list(sql_enum) == ['a']


@pytest.mark.SqlEnum
def test_extend():
    sql_enum = SqlEnum()
    assert len(sql_enum) == 0
    sql_enum.extend(['a', 'b'])
    assert len(sql_enum) == 2
    assert list(sql_enum) == ['a', 'b']


@pytest.mark.SqlEnum
def test_pop():
    sql_enum = SqlEnum('a')
    assert len(sql_enum) == 1
    assert sql_enum.pop() == 'a'
    assert len(sql_enum) == 0


@pytest.mark.SqlEnum
def test_clear():
    sql_enum = SqlEnum('a', 'b')
    assert len(sql_enum) == 2
    sql_enum.clear()
    assert len(sql_enum) == 0


@pytest.mark.SqlEnum
def test_index():
    sql_enum = SqlEnum('a', 'b')
    assert sql_enum.index('b') == 1


@pytest.mark.SqlEnum
def test_sort():
    sql_enum = SqlEnum('b', 'a')
    sql_enum.sort()
    assert list(sql_enum) == ['a', 'b']


@pytest.mark.SqlEnum
def test_reverse():
    sql_enum = SqlEnum('a', 'b')
    sql_enum.reverse()
    assert list(sql_enum) == ['b', 'a']

@pytest.mark.SqlEnum
def test_insert():
    sql_enum = SqlEnum('a', 'b')
    sql_enum.insert(0, 'c')
    assert list(sql_enum) == ['c', 'a', 'b']


@pytest.mark.SqlEnum
def test_remove():
    sql_enum = SqlEnum('a', 'b')
    sql_enum.remove('a')
    assert list(sql_enum) == ['b']


@pytest.mark.SqlEnum
def test_count():
    sql_enum = SqlEnum('a', 'a')
    assert sql_enum.count('a') == 2


@pytest.mark.SqlEnum
def test_copy():
    sql_enum = SqlEnum('a', 'b')
    assert list(sql_enum.copy()) == ['a', 'b']
