import pytest
import uuid
from sqlconstructor import SqlQuery, SqlCols, SqlVals, SqlEnum
from fixtures.expected_examples import (
    insert_into_inline_using_cols_sql,
    insert_into_multiline_using_cols_sql,
    insert_into_inline_using_sqlenum_sql,
    insert_into_multiline_using_sqlenum_sql,
)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlCols
@pytest.mark.SqlVals
def test_insert_into_use_cols_str_and_vals_str(insert_into_multiline_using_cols_sql):
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlCols(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        ),
    )
    q['values'](
        SqlVals(
            1,
            'phone',
            _uuid,
        ),
    )
    container = q()
    assert str(container) == insert_into_multiline_using_cols_sql.format(uuid=_uuid)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlCols
@pytest.mark.SqlVals
def test_insert_into_use_cols_multiline_wrap_and_vals_multiline_wrap(
    insert_into_multiline_using_cols_sql,
):
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlCols(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        ).multiline().wrap(),
    )
    q['values'](
        SqlVals(
            1,
            'phone',
            _uuid,
        ).multiline().wrap(),
    )
    container = q()
    assert str(container) == insert_into_multiline_using_cols_sql.format(uuid=_uuid)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlCols
@pytest.mark.SqlVals
def test_insert_into_use_cols_inline_wrap_and_vals_multiline_wrap(
    insert_into_inline_using_cols_sql,
):
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlCols(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        ).inline().wrap(),
    )
    q['values'](
        SqlVals(
            1,
            'phone',
            _uuid,
        ).inline().wrap(),
    )
    container = q()
    assert str(container) == insert_into_inline_using_cols_sql.format(uuid=_uuid)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlCols
@pytest.mark.SqlVals
def test_insert_into_use_sql_enum_multiline_wrap_and_vals_multiline_wrap(
    insert_into_multiline_using_sqlenum_sql,
):
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlEnum(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        )
        .multiline()
        .wrap(),
    )
    q['values'](
        SqlVals(
            1,
            'phone',
            _uuid,
        )
        .multiline()
        .wrap(),
    )
    container = q()
    assert str(container) == insert_into_multiline_using_sqlenum_sql.format(uuid=_uuid)


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlCols
@pytest.mark.SqlVals
def test_insert_into_use_sql_enum_inline_wrap_and_vals_inline_wrap(
    insert_into_inline_using_sqlenum_sql,
):
    q = SqlQuery()
    _uuid = uuid.uuid4()
    q['insert into'](
        'product',
        SqlEnum(
            'brand_id',
            'name',
            'quality',
            'uuid_id',
        )
        .inline()
        .wrap(),
    )
    q['values'](
        SqlVals(
            1,
            'phone',
            _uuid,
        )
        .inline()
        .wrap(),
    )
    container = q()
    assert str(container) == insert_into_inline_using_sqlenum_sql.format(uuid=_uuid)
