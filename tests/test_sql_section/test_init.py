import pytest
from sqlconstructor import SqlSection

SECTION_HEADER = 'select'


@pytest.mark.SqlSection
@pytest.mark.parametrize("args, kwargs", [
    ([SECTION_HEADER], {}),
    ([], {'section_header': SECTION_HEADER}),
])
def test_init_with_section_header(args, kwargs):
    section = SqlSection(*args, **kwargs)
    assert section.section_header == SECTION_HEADER
    assert section.container is None
