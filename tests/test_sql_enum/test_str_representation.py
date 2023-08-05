import pytest
from sqlconstructor import SqlEnum


@pytest.mark.SqlEnum
def test_string_representation_one_element():
    assert (
        str(
            SqlEnum(
                'brand_id',
            )
        )
        == '(\n  brand_id\n)'
    )


@pytest.mark.SqlEnum
def test_string_representation_two_and_more_elements():
    assert (
        str(
            SqlEnum(
                'brand_id',
                'name',
            )
        )
        == '(\n  brand_id,\n  name\n)'
    )
