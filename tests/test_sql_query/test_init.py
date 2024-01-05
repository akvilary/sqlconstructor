import pytest
from sqlconstructor import SqlQuery, SqlEnum, SqlVal, SqlSectionHeader

from fixtures.expected_examples import simple_query_sql
from fixtures.simple_query_dict import simple_query_dict


@pytest.mark.SqlQuery
def test_init_with_no_args():
    q = SqlQuery()
    assert isinstance(q, SqlQuery)


@pytest.mark.SqlQuery
def test_init_with_sql_id():
    sql_id = 'abc'
    q = SqlQuery(sql_id=sql_id)
    assert q.sql_id == sql_id
    assert str(q()) == f"-- sql_id='{sql_id}'"


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.SqlSectionHeader
def test_init_query_by_dict(simple_query_dict, simple_query_sql):
    q = SqlQuery(simple_query_dict)
    assert len(q) == 3
    container = q()
    assert str(container) == simple_query_sql


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_init_query_by_dict_with_empty_body():
    h = SqlSectionHeader
    query_dict = {
        h('SELECT'): 1,
        h('UNION'): None,
        h('SELECT'): 2,
    }
    q = SqlQuery(query_dict)
    assert len(q) == 3
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  1',
            'UNION',
            'SELECT',
            '  2',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_init_query_by_dict_and_sql_cols_instance(simple_query_sql):
    q = SqlQuery(
        {
            'select': SqlEnum('id', 'name').multiline(),
            'from': 'product',
            'where': (
                "quality = 'Best'",
                'and brand_id = 1',
            ),
        }
    )
    assert len(q) == 3
    container = q()
    assert str(container) == simple_query_sql


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.SqlSectionHeader
def test_init_query_by_dict_and_sql_section_header_with_duplicates():
    H = SqlSectionHeader
    q = SqlQuery(
        {
            H('select'): True,
            '': 'union all',
            H('select'): True,
        }
    )
    assert len(q) == 3
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  TRUE',
            'UNION ALL',
            'SELECT',
            '  TRUE',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.SqlSectionHeader
def test_init_query_by_dict_and_sql_section_header_with_duplicates_and_sql_vals():
    H = SqlSectionHeader
    hello = 'hello'
    q = SqlQuery(
        {
            H('select'): f"'{hello}'",
            '': 'union all',
            H('select'): SqlVal(hello),
            H(): 'union all',
            H('select'): f"'{hello}'",
        }
    )
    assert len(q) == 5
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            f"  '{hello}'",
            'UNION ALL',
            'SELECT',
            f"  '{hello}'",
            'UNION ALL',
            'SELECT',
            f"  '{hello}'",
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_init_query_by_dict_and_nested_dict():
    q = SqlQuery(
        {
            'select': (
                'p.id',
                'p.name',
            ),
            'from': 'product as p',
            'left join lateral': {
                'select': (
                    'e.id',
                    'e.expiration_date',
                ),
                'from': 'expiration as e',
                'where': (
                    'p.id = e.id',
                    'AND e.expiration_date <= now()',
                ),
                '__wrapper_text__': 'as exp on true',
            },
            'where': (
                "quality = 'Best'",
                'and brand_id = 1',
            ),
        }
    )
    assert len(q) == 4
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  p.id,',
            '  p.name',
            'FROM',
            '  product AS p',
            'LEFT JOIN LATERAL',
            '  (',
            '    SELECT',
            '      e.id,',
            '      e.expiration_date',
            '    FROM',
            '      expiration AS e',
            '    WHERE',
            '      p.id = e.id',
            '      AND e.expiration_date <= now()',
            '  ) AS exp ON TRUE',
            'WHERE',
            "  quality = 'Best'",
            '  AND brand_id = 1',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_init_query_by_dict_with_cte():
    q = SqlQuery(
        {
            'products': {
                '__is_cte__': True,
                'select': 'product_id',
                'from': 'warehouse',
                'where': 'quantity > 0',
            },
            'select': 'product_id',
            'from': 'products',
        }
    )
    assert len(q) == 3
    container = q()
    assert str(container) == '\n'.join(
        (
            'WITH products AS',
            '  (',
            '    SELECT',
            '      product_id',
            '    FROM',
            '      warehouse',
            '    WHERE',
            '      quantity > 0',
            '  )',
            'SELECT',
            '  product_id',
            'FROM',
            '  products',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
@pytest.mark.parametrize(
    'query_dict_with_ctes',
    [
        {
            '__ctes__': {
                'products': {
                    'select': 'product_id',
                    'from': 'warehouse',
                    'where': 'quantity > 0',
                },
            },
            'select': 'product_id',
            'from': 'products',
        },
        {
            'select': 'product_id',
            'from': 'products',
            '__ctes__': {
                'products': {
                    'select': 'product_id',
                    'from': 'warehouse',
                    'where': 'quantity > 0',
                },
            },
        },
    ],
)
def test_init_query_by_dict_with_ctes_in_one_nested_dict(query_dict_with_ctes):
    q = SqlQuery(query_dict_with_ctes)
    assert len(q) == 3
    container = q()
    assert str(container) == '\n'.join(
        (
            'WITH products AS',
            '  (',
            '    SELECT',
            '      product_id',
            '    FROM',
            '      warehouse',
            '    WHERE',
            '      quantity > 0',
            '  )',
            'SELECT',
            '  product_id',
            'FROM',
            '  products',
        )
    )


@pytest.mark.SqlQuery
def test_init_with_sections_default_kwargs():
    q = SqlQuery(header_end=' ', sep=' +', line_end=' ', do_upper_keywords=False)
    q['select'](
        'a',
        'b',
    )
    assert str(q()) == 'select a + b'
