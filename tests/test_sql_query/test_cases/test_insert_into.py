import pytest
import uuid
from sqlconstructor import SqlQuery, Cols, Vals, SqlEnum


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
            'uuid_id',
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
        '    "uuid_id"\n'
        '  )\n'
        'VALUES\n'
        '  (\n'
        '    1,\n'
        "    'phone',\n"
        f"    '{_uuid}'\n"
        '  )'
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.Cols
@pytest.mark.Vals
def test_insert_into_use_sql_enum_inline_wrap_and_vals_inline_wrap():
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlEnum(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        ).inline().wrap(),
    )
    q['values'](
        Vals(
            1,
            'phone',
            _uuid,
        ).inline().wrap(),
    )
    container = q()
    assert (
        str(container) == f'INSERT INTO\n'
        '  product\n'
        '  (\n'
        '    brand_id, name, quality, uuid_id\n'
        '  )\n'
        'VALUES\n'
        '  (\n'
        f"    1, 'phone', '{_uuid}'\n"
        '  )'
    )
