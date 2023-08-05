import pytest
from sqlconstructor import SqlCols


def test_inline_one_element():
    assert (
        str(
            SqlCols(
                'brand_id',
            ).inline()
        )
        == '"brand_id"'
    )


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


def test_inline_wrap_one_element():
    assert (
        str(
            SqlCols(
                'brand_id',
            ).inline().wrap()
        )
        == '(\n  "brand_id"\n)'
    )


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
