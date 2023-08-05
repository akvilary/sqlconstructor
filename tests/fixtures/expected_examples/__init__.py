import pytest
import os

CURRENT_DIR = os.path.dirname(__file__)


def get_file_path(file_name):
    return os.path.join(CURRENT_DIR, file_name)


@pytest.fixture
def simple_query_sql():
    file_path = get_file_path('simple_query.sql')
    with open(file_path, encoding='utf-8', newline='') as file:
        sql_file = file.read()
        # skip added '\n' character by read method
        return sql_file[:-1]


