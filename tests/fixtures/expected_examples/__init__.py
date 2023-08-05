import pytest
import os

CURRENT_DIR = os.path.dirname(__file__)


def get_file_path(file_name):
    return os.path.join(CURRENT_DIR, file_name)


def read_file_without_newline_at_the_end(file_name: str) -> str:
    file_path = get_file_path(file_name)
    with open(file_path, encoding='utf-8', newline='') as file:
        sql_file = file.read()
        # skip added '\n' character by read method
        return sql_file.rstrip()


@pytest.fixture
def simple_query_sql():
    return read_file_without_newline_at_the_end('simple_query.sql')


@pytest.fixture
def select_section_of_simple_query_sql():
    return read_file_without_newline_at_the_end('select_section_of_simple_query.sql')


@pytest.fixture
def insert_into_inline_using_cols_sql():
    return read_file_without_newline_at_the_end('insert_into_inline_using_cols.sql')


@pytest.fixture
def insert_into_multiline_using_cols_sql():
    return read_file_without_newline_at_the_end('insert_into_multiline_using_cols.sql')


@pytest.fixture
def insert_into_inline_using_sqlenum_sql():
    return read_file_without_newline_at_the_end('insert_into_inline_using_sqlenum.sql')


@pytest.fixture
def insert_into_multiline_using_sqlenum_sql():
    return read_file_without_newline_at_the_end('insert_into_multiline_using_sqlenum.sql')
