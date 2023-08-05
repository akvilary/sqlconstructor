import pytest
from sqlconstructor import SqlEnum


def test_inline_one_element():
    assert (
        str(
            SqlEnum(
                'brand_id',
            ).inline()
        )
        == 'brand_id'
    )


def test_inline_one_element_case_int():
    assert (
        str(
            SqlEnum(
                1,
            ).inline()
        )
        == '1'
    )


def test_inline_two_and_more_elements():
    assert (
        str(
            SqlEnum(
                'brand_id',
                'name',
            ).inline()
        )
        == 'brand_id, name'
    )


def test_inline_wrap_one_element():
    assert (
        str(
            SqlEnum(
                'brand_id',
            ).inline().wrap()
        )
        == '(\n  brand_id\n)'
    )


def test_inline_wrap_two_and_more_elements():
    assert (
        str(
            SqlEnum(
                'brand_id',
                'name',
            ).inline().wrap()
        )
        == '(\n  brand_id, name\n)'
    )
