import pytest


@pytest.fixture
def simple_query_dict():
    return {
        'select': (
            'id',
            'name',
        ),
        'from': 'product',
        'where': (
            "quality = 'Best'",
            'and brand_id = 1',
        ),
    }


@pytest.fixture
def simple_query_dict_with_placeholders():
    return {
        'select': (
            'id',
            'name',
        ),
        'from': 'product',
        'where': (
            'quality = $quality',
            'AND brand_id = $brand_id',
        ),
    }
