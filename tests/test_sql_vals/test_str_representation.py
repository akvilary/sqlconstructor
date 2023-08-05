import pytest
import uuid
from sqlconstructor import SqlVals


@pytest.mark.SqlVals
def test_string_representation_one_element():
    assert (
        str(
            SqlVals(
                1,
            )
        )
        == '(\n  1\n)'
    )


@pytest.mark.SqlVals
def test_string_representation_two_and_more_elements():
    _uuid = uuid.uuid4()
    assert (
        str(
            SqlVals(
                1,
                'phone',
                _uuid,
            )
        )
        == f"(\n  1,\n  'phone',\n  '{_uuid}'\n)"
    )
