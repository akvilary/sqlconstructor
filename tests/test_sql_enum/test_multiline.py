import pytest
from sqlconstructor import SqlEnum


@pytest.mark.SqlEnum
def test_multiline_one_element():
    assert (
        str(
            SqlEnum(
                'brand_id',
            ).multiline()
        )
        == 'brand_id'
    )


@pytest.mark.SqlEnum
def test_multiline_two_and_more_elements():
    assert (
        str(
            SqlEnum(
                'brand_id',
                'name',
            ).multiline()
        )
        == 'brand_id,\nname'
    )


@pytest.mark.SqlEnum
def test_multiline_wrap_one_element():
    assert (
        str(
            SqlEnum(
                'brand_id',
            ).multiline().wrap()
        )
        == '(\n  brand_id\n)'
    )


@pytest.mark.SqlEnum
def test_multiline_wrap_two_and_more_elements():
    assert (
        str(
            SqlEnum(
                'brand_id',
                'name',
            ).multiline().wrap()
        )
        == '(\n  brand_id,\n  name\n)'
    )
