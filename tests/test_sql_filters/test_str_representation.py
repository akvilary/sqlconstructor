import pytest
import uuid
from sqlconstructor import SqlFilters, AND, OR


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
    assert str(filters) == expected_result.format(mode=AND, uuid=_uuid)


@pytest.mark.SqlFilters
def test_string_representation_and_mode(dict_for_filters, expected_result):
    _uuid = dict_for_filters['identifier']
    filters = SqlFilters(dict_for_filters, AND)
    assert str(filters) == expected_result.format(mode=AND, uuid=_uuid)


@pytest.mark.SqlFilters
def test_string_representation_or_mode(dict_for_filters, expected_result):
    _uuid = dict_for_filters['identifier']
    filters = SqlFilters(dict_for_filters, OR)
    assert str(filters) == expected_result.format(mode=OR, uuid=_uuid)


@pytest.mark.SqlFilters
def test_filters_and_mode_as_keyword_arguments():
    filters = SqlFilters(None, OR, filters='a', mode='b')
    assert str(filters) == '\n'.join(
        (
            "filters='a'",
            OR,
            "mode='b'",
        )
    )
