import pytest
from sqlconstructor import (
    SqlContainer,
    SqlVal,
    SqlCol,
    SqlCols,
    SqlEnum,
    SqlFilter,
    SqlFilters,
    SqlPlaceholder,
    SqlSectionHeader,
    AND
)


@pytest.mark.SqlVal
@pytest.mark.SqlContainer
def test_convert_sql_container():
    assert str(SqlVal(SqlContainer('product'))) == 'product'


@pytest.mark.SqlVal
@pytest.mark.SqlContainer
def test_convert_sql_container_in_dict_value():
    assert str(SqlVal({'a': SqlContainer('product')})) == """E'{"a": "product"}'"""


@pytest.mark.SqlVal
@pytest.mark.SqlCol
def test_convert_sql_col():
    assert str(SqlVal(SqlCol('product'))) == '"product"'


@pytest.mark.SqlVal
@pytest.mark.SqlCol
def test_convert_sql_col_in_dict_value():
    assert str(SqlVal({'a': SqlCol('product')})) == """E'{"a": "\\\\"product\\\\""}'"""


@pytest.mark.SqlVal
@pytest.mark.SqlCols
def test_convert_sql_cols():
    assert str(SqlVal(SqlCols('product', 'quantity'))) == '"product", "quantity"'


@pytest.mark.SqlVal
@pytest.mark.SqlContainer
def test_convert_sql_cols_in_dict_value():
    cols = SqlCols('product', 'quantity')

    result = str(SqlVal({'a': cols}))
    expected_result = """E'{"a": ["\\\\"product\\\\"", "\\\\"quantity\\\\""]}'"""
    assert result == expected_result


@pytest.mark.SqlVal
@pytest.mark.SqlEnum
def test_convert_sql_enum():
    assert str(SqlVal(SqlEnum('product', 'quantity'))) == 'product, quantity'


@pytest.mark.SqlVal
@pytest.mark.SqlEnum
def test_convert_sql_enum_in_dict_value():
    assert (
        str(SqlVal({'a': SqlEnum('product', 'quantity')}))
        == """E'{"a": ["product", "quantity"]}'"""
    )


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_as_string():
    assert str(SqlVal(SqlFilter('product'))) == 'product'


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_as_string_in_dict_value():
    assert str(SqlVal({'a': SqlFilter('product')})) == """E'{"a": "product"}'"""


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_as_dict():
    assert str(SqlVal(SqlFilter({'product_name': 'tv'}))) == "product_name='tv'"


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_as_dict_in_dict_value():
    _filter = SqlFilter({'product_name': 'tv'})
    val = SqlVal({'a': _filter})
    assert (
        str(val)
        == """E'{"a": "product_name=\\\'tv\\\'"}'"""
    )


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_with_kwarg():
    assert str(SqlVal(SqlFilter(product_name='tv'))) == "product_name='tv'"


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filter_with_kwarg_in_dict_value():
    assert (
        str(SqlVal({'a': SqlFilter(product_name='tv')}))
        == """E'{"a": "product_name=\\\'tv\\\'"}'"""
    )


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filters():
    assert str(SqlVal(SqlFilters({'product_name': 'tv', 'quality': 'Best'}))) == '\n'.join(
        (
            "product_name='tv'",
            AND,
            "quality='Best'",
        )
    )


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_filters_in_dict_value():
    assert (
        str(SqlVal({'a': SqlFilters({'product_name': 'tv', 'quality': 'Best'})}))
        == """E'{"a": """
        + '\\n'.join(
            (
                "\"product_name='tv'",
                AND,
                "quality='Best'\"",
            )
        )
        + "}'"
    )


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_placeholder():
    assert str(SqlVal(SqlPlaceholder('brand_id'))) == '$brand_id'


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_placeholder_in_dict_value():
    assert str(SqlVal({'a': SqlPlaceholder('brand_id')})) == """E'{"a": "$brand_id"}'"""


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_section_header():
    assert str(SqlVal(SqlSectionHeader('select'))) == 'select'


@pytest.mark.SqlVal
@pytest.mark.SqlFilter
def test_convert_sql_section_header_in_dict():
    assert str(SqlVal({'a': SqlSectionHeader('select')})) == """E'{"a": "select"}'"""
