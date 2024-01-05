import pytest
from sqlconstructor import SqlQuery, SqlContainer
from fixtures.expected_examples import select_section_of_simple_query_sql


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple():
    q = SqlQuery()
    q.add('abc xyz')
    container = q()
    assert str(container) == 'abc xyz'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple_to_filled_query(select_section_of_simple_query_sql):
    q = SqlQuery()
    q['select'](
        'id',
        'name',
    )
    q.add('abc xyz')
    container = q()
    assert str(container) == (select_section_of_simple_query_sql + '\nabc xyz')


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple_by_magic_add():
    q = _q = SqlQuery()
    q += 'abc xyz'
    container = q()
    assert str(container) == 'abc xyz'
    assert q is _q


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_inherit_vars_of_containers_in_add_method():
    q = SqlQuery()
    subquery = SqlQuery()
    subquery['select']('$id', '$name')(id=1, name='phone')
    subquery_container = subquery()
    q += subquery_container
    query_container = q()
    assert query_container.vars == subquery_container.vars
    assert query_container.dumps() == "SELECT\n  1,\n  'phone'"


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_str_with_positive_indentation():
    q = SqlQuery()
    q.add('a', ind=2)
    container = q()
    assert str(container) == '  a'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_str_with_negative_indentation():
    q = SqlQuery()
    q.add('  a', ind=-4)
    container = q()
    assert str(container) == 'a'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_container_with_positive_indentation():
    q = SqlQuery()
    q.add(SqlContainer('a'), ind=2)
    container = q()
    assert str(container) == '  a'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_container_with_negative_indentation():
    q = SqlQuery()
    q.add(SqlContainer('  a'), ind=-4)
    container = q()
    assert str(container) == 'a'


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_simple_query_dict():
    q = SqlQuery()
    query_dict = {'select': 'a'}
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  a',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_query_dict_with_nested_dict():
    q = SqlQuery()
    query_dict = {
        'select': {
            'exists': '1',
        },
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(('SELECT', '  EXISTS', '    1'))


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_query_dict_with_nested_subquery_dict():
    q = SqlQuery()
    query_dict = {
        'select': {
            'select exists': '1',
            '__do_wrap__': True,
        },
    }
    q.add(query_dict)

    assert len(q) == 1

    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  (',
            '    SELECT EXISTS',
            '      1',
            '  )',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_query_dict_with_cte_dict():
    q = SqlQuery()
    query_dict = {
        'best_products': {
            '__is_cte__': True,
            'select': 'id',
            'from': 'product',
            'where': "quality = 'Best'",
        },
        'select': 'id',
        'from': 'best_products',
    }
    q.add(query_dict)

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
def test_add_query_dict_with_ctes_dict():
    q = SqlQuery()
    query_dict = {
        '__ctes__': {
            'best_products': {
                'select': 'id',
                'from': 'product',
                'where': "quality = 'Best'",
            },
        },
        'select': 'id',
        'from': 'best_products',
    }
    q.add(query_dict)

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
def test_add_dict_with_positive_indetation():
    q = SqlQuery()
    query_dict = {'select': 'a'}
    q.add(query_dict, ind=2)
    container = q()
    assert str(container) == '\n'.join(
        (
            '  SELECT',
            '    a',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_negative_indetation():
    q = SqlQuery()
    query_dict = {'  select': '    a'}
    q.add(query_dict, ind=-4)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  a',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_custom_separator():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__sep__': '\n  +',
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  a',
            '  +',
            '  b',
        )
    )

@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_custom_line_end():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__line_end__': '',
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '  a,b',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_custom_header_ind():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__line_end__': '',
        '__header_ind__': 1,
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            ' SELECT',
            '  a,b',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_custom_body_ind():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__line_end__': '',
        '__body_ind__': 3,
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '   a,b',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_custom_body_ind_with_space_line_end():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__line_end__': ' ',
        '__body_ind__': 3,
    }
    q.add(query_dict)
    container = q()
    assert str(container) == '\n'.join(
        (
            'SELECT',
            '   a, b',
        )
    )


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_add_dict_with_sep_and_line_end_and_header_end_and_do_not_upper_keywords():
    q = SqlQuery()
    query_dict = {
        'select': (
            'a',
            'b',
        ),
        '__header_end__': ' ',
        '__sep__': '+',
        '__line_end__': '',
        '__do_upper_keywords__': False,
    }
    q.add(query_dict)
    container = q()
    assert str(container) == 'select a+b'
