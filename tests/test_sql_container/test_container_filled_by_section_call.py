import pytest
from sqlconstructor import SqlSection
from fixtures.expected_examples import select_section_of_simple_query_sql


@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_check_container_text_after_calling_section(select_section_of_simple_query_sql):
    section = SqlSection('select')
    section(
        'id',
        'name',
    )
    assert section.container.text == select_section_of_simple_query_sql
