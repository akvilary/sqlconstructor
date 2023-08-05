import pytest
from sqlconstructor import SqlQuery, SqlContainer, SqlCte


@pytest.mark.SqlQuery
@pytest.mark.SqlContainer
@pytest.mark.SqlCte
def test_build_query_by_dict():
    query_dict = {
        'select': (
            'id',
            'name',
        ),
        'from': 'product',
    }
    query = SqlQuery(query_dict)
    container = query()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  id,',
            '  name',
            'FROM',
            '  product',
        )
    )


def test_build_query_by_dict_with_ctes():
    query_dict = {
        'products': {
            '__is_cte__': True,
            'select': 'product_id',
            'from': 'warehouse',
            'where': 'quantity > 0',
        },
        'prices': {
            '__is_cte__': True,
            'select': 'price',
            'from': 'catalog',
        },
        'select': (
            'id',
            'name',
        ),
        'from': 'product',
        'where': 'id in (select product_id from products)',
    }
    query = SqlQuery(query_dict)
    container = query()
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
            '  ),',
            'prices AS',
            '  (',
            '    SELECT',
            '      price',
            '    FROM',
            '      catalog',
            '  )',
            'SELECT',
            '  id,',
            '  name',
            'FROM',
            '  product',
            'WHERE',
            '  id IN (SELECT product_id FROM products)',
        )
    )


def test_build_query_by_dict_with_nested_dict_subquery():
    query_dict = {
        'select': {
            'select': 'a',
            'from': 'b',
            '__do_wrap__': True,
        },
    }
    query = SqlQuery(query_dict)
    container = query()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  (',
            '    SELECT',
            '      a',
            '    FROM',
            '      b',
            '  )',
        )
    )


def test_build_query_by_dict_with_nested_dict_subquery_with_wrapper_text():
    query_dict = {
        'select': {
            'select': 'a',
            'from': 'b',
            '__wrapper_text__': 'as c on true',
        },
    }
    query = SqlQuery(query_dict)
    container = query()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  (',
            '    SELECT',
            '      a',
            '    FROM',
            '      b',
            '  ) AS c ON TRUE',
        )
    )
