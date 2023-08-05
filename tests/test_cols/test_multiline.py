import pytest
from sqlconstructor import Cols


def test_multiline_one_element():
    assert (
        str(
            Cols(
                'brand_id',
            ).multiline()
        )
        == '"brand_id"'
    )


def test_multiline_two_and_more_elements():
    assert (
        str(
            Cols(
                'brand_id',
                'name',
            ).multiline()
        )
        == '"brand_id",\n"name"'
    )


def test_multiline_wrap_one_element():
    assert (
        str(
            Cols(
                'brand_id',
            ).multiline().wrap()
        )
        == '(\n  "brand_id"\n)'
    )


def test_multiline_wrap_two_and_more_elements():
    assert (
        str(
            Cols(
                'brand_id',
                'name',
            ).multiline().wrap()
        )
        == '(\n  "brand_id",\n  "name"\n)'
    )
