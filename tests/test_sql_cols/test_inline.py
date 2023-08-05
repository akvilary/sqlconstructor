import pytest
from sqlconstructor import SqlCols


@pytest.mark.SqlCols
def test_inline_one_element():
    assert (
        str(
            SqlCols(
                'brand_id',
            ).inline()
        )
        == '"brand_id"'
    )


@pytest.mark.SqlCols
def test_inline_two_and_more_elements():
    assert (
        str(
            SqlCols(
                'brand_id',
                'name',
            ).inline()
        )
        == '"brand_id", "name"'
    )


@pytest.mark.SqlCols
def test_inline_wrap_one_element():
    assert (
        str(
            SqlCols(
                'brand_id',
            ).inline().wrap()
        )
        == '(\n  "brand_id"\n)'
    )


@pytest.mark.SqlCols
def test_inline_wrap_two_and_more_elements():
    assert (
        str(
            SqlCols(
                'brand_id',
                'name',
            ).inline().wrap()
        )
        == '(\n  "brand_id", "name"\n)'
    )
