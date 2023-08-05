import pytest
from sqlconstructor import SqlQuery, SqlSection


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
def test_getitem_by_int():
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q['from']('product')
    assert len(q) == 2
    assert str(q[0]) == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name',
        )
    )
    assert str(q[1]) == '\n'.join(
        (
            'FROM',
            '  product',
        )
    )
