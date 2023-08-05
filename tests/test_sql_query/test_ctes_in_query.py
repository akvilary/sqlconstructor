import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_query_ctes_reg_by_dict():
    q = SqlQuery(
        {
            'select': 'id',
            'from': 'best_products',
        }
    )
    q.ctes.reg(
        'best_products',
        {
            'select': 'id',
            'from': 'product',
            'where': "quality = 'Best'",
        },
    )

    assert len(q) == 3
    assert len(q.data) == 2
    assert len(q.ctes) == 1

    container = q()
    assert str(container) == '\n'.join(
        (
            'WITH best_products AS',
            '  (',
            '    SELECT',
            '      id',
            '    FROM',
            '      product',
            '    WHERE',
            "      quality = 'Best'",
            '  )',
            'SELECT',
            '  id',
            'FROM',
            '  best_products',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_query_ctes_setitem_by_dict():
    q = SqlQuery(
        {
            'select': 'id',
            'from': 'best_products',
        }
    )
    q.ctes['best_products'] = {
        'select': 'id',
        'from': 'product',
        'where': "quality = 'Best'",
    }

    assert len(q) == 3
    assert len(q.data) == 2
    assert len(q.ctes) == 1

    container = q()
    assert str(container) == '\n'.join(
        (
            'WITH best_products AS',
            '  (',
            '    SELECT',
            '      id',
            '    FROM',
            '      product',
            '    WHERE',
            "      quality = 'Best'",
            '  )',
            'SELECT',
            '  id',
            'FROM',
            '  best_products',
        )
    )
