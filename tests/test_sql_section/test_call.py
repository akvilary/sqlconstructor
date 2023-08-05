import pytest
from sqlconstructor import SqlQuery


@pytest.mark.SqlQuery
@pytest.mark.SqlSection
@pytest.mark.SqlContainer
def test_check_container_of_section_after_calling_section():
    q = SqlQuery()
    section = q['select']
    container = section(
        'id',
        'name',
    )
    assert section.container is not None
    assert section.container is container
