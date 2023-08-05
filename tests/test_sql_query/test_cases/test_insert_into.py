import pytest
import uuid
from sqlconstructor import SqlQuery, Cols, Vals


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.Cols
@pytest.mark.Vals
def test_insert_into():
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        Cols(
            'brand_id',
            'name',
            'quality',
            'uuid',
        ),
    )
    q['values'](
        Vals(
            1,
            'phone',
            _uuid,
        )
    )
    container = q()
    assert (
        str(container) == f'INSERT INTO\n'
        '  product\n'
        '  (\n'
        '    "brand_id",\n'
        '    "name",\n'
        '    "quality",\n'
        '    "uuid"\n'
        '  )\n'
        'VALUES\n'
        '  (\n'
        '    1,\n'
        "    'phone',\n"
        f"    '{_uuid}'\n"
        '  )'
    )
