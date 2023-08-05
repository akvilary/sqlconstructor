import pytest
import uuid
from sqlconstructor import SqlFilters
from sqlconstructor.constants import AND_MODE, OR_MODE


@pytest.fixture
def dict_for_filters():
    return {
        'id': 1,
        'name': 'hello',
        'enable': True,
        'identifier': uuid.uuid4(),
    }


@pytest.fixture
def expected_result():
    return '\n'.join(
        (
            'id=1',
            '{mode}',
            "name='hello'",
            '{mode}',
            'enable=True',
            '{mode}',
            "identifier='{uuid}'",
        )
    )


@pytest.mark.SqlFilters
def test_string_representation_empty_filters_default_mode():
    filters = SqlFilters()
    assert str(filters) == ''


@pytest.mark.SqlFilters
def test_string_representation_default_mode(dict_for_filters, expected_result):
    _uuid = dict_for_filters['identifier']
    filters = SqlFilters(dict_for_filters)
    assert str(filters) == expected_result.format(mode=AND_MODE, uuid=_uuid)


@pytest.mark.SqlFilters
def test_string_representation_and_mode(dict_for_filters, expected_result):
    _uuid = dict_for_filters['identifier']
    filters = SqlFilters(dict_for_filters, AND_MODE)
    assert str(filters) == expected_result.format(mode=AND_MODE, uuid=_uuid)


@pytest.mark.SqlFilters
def test_string_representation_or_mode(dict_for_filters, expected_result):
    _uuid = dict_for_filters['identifier']
    filters = SqlFilters(dict_for_filters, OR_MODE)
    assert str(filters) == expected_result.format(mode=OR_MODE, uuid=_uuid)


@pytest.mark.SqlFilters
def test_filters_and_mode_as_keyword_arguments():
    filters = SqlFilters(None, OR_MODE, filters='a', mode='b')
    assert str(filters) == '\n'.join(
        (
            "filters='a'",
            OR_MODE,
            "mode='b'",
        )
    )
