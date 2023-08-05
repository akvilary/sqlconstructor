import pytest
from sqlconstructor import SqlQuery, SqlSection


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
def test_getitem_by_slice():
    a = SqlQuery()
    a['select'](
        'id',
        'name',
    )
    a['from']('product')
    a['where']('quantity > 0')
    assert len(a) == 3
    b = a[:-1]
    assert b is not a
    assert len(b) == 2
    iter_of_a = iter(a)
    iter_of_b = iter(b)
    for _ in range(2):
        assert next(iter_of_a) is next(iter_of_b)
    assert str(b()) == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name',
            'FROM',
            '  product'
        )
    )
