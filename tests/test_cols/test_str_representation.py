import pytest
from sqlconstructor import Cols


def test_string_representation_one_element():
    assert (
        str(
            Cols(
                'brand_id',
            )
        )
        == '(\n  "brand_id"\n)'
    )


def test_string_representation_two_and_more_elements():
    assert (
        str(
            Cols(
                'brand_id',
                'name',
            )
        )
        == '(\n  "brand_id",\n  "name"\n)'
    )
