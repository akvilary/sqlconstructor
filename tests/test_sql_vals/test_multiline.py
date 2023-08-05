import pytest
import uuid
from sqlconstructor import SqlVals


@pytest.mark.SqlVals
def test_multiline_one_element():
    assert (
        str(
            SqlVals(
                1,
            ).multiline()
        )
        == '1'
    )


@pytest.mark.SqlVals
def test_multiline_two_and_more_elements():
    _uuid = uuid.uuid4()
    assert (
        str(
            SqlVals(
                1,
                'phone',
                _uuid,
            ).multiline()
        )
        == f"1,\n'phone',\n'{_uuid}'"
    )


@pytest.mark.SqlVals
def test_multiline_wrap_one_element():
    assert (
        str(
            SqlVals(
                1,
            ).multiline().wrap()
        )
        == '(\n  1\n)'
    )


@pytest.mark.SqlVals
def test_multiline_wrap_two_and_more_elements():
    _uuid = uuid.uuid4()
    assert (
        str(
            SqlVals(
                1,
                'phone',
                _uuid,
            ).multiline().wrap()
        )
        == f"(\n  1,\n  'phone',\n  '{_uuid}'\n)"
    )
